from datetime import datetime
import multiprocessing
from pickle import LIST
import threading
from time import sleep
import warnings
from const import CONFIG_FILE, LIST_COSTS, READABLE_TIME_FORMAT, SECOND, SLEEP, USAGE_FILE, TIME_FORMAT
import const
from debug import save_print_dbg
from decorator import go_main_screen, if_auto_run_then_wait_town, sleep_decorator
from error import EmptyBaitException, InvalidValueValidateException, NoEnergyException, UnableJoinException
from utils import get_json_file, is_rerun_mode, save_json_file
from window import get_app


class Farm(object):
    feature = None
    configUI = None
    name = None
    thread = None
    process = None
    debug = None
    run_time = 0
    total_run = 0
    start_time = None

    def __init__(self):
        self.reset_config()

    def hard_reset_config(self):
        self.reset_config()
        self.thread = None

    def reset_config(self):
        self.run_time = 0
        self.total_selected_cost = 0
        self.start_time = None
        self.set_name()
        self.get_config()
        self.mapping_config()
        self.validate()

    def set_name(self):
        _t = self.feature.replace(' ', '_')
        self.name = datetime.now().strftime(f'{TIME_FORMAT}_{_t}')

    def decorator_catch_exceptions(f):
        def wrapper(self):
            err = ''
            special = False
            try:
                f(self)
                return True
            except NoEnergyException:
                if self.is_smart_rerun_energy():
                    if not self.rerun_mode:  # in case of smart rerun enabled
                        special = True
                    else:
                        return wrapper(self)
                err = NoEnergyException(feature=str(self.feature))
            except KeyboardInterrupt:
                err = f"'{self.feature}' stopped by keyboard"
            except EmptyBaitException as ex:
                err = str(ex)
            except UnableJoinException as ex:
                err = str(ex)
                special = True
            except Exception as ex:
                err = f"got error when run '{self.feature}': {str(ex)}"
            save_print_dbg(txt=err)
            return True if special else False
        return wrapper

    def decorator_init(f):
        def wrapper(self):
            get_app()
            self.start_time = datetime.now()
            save_print_dbg(f"Running '{self.feature}'")
            save_print_dbg(f"\n***Debug for '{self.name}'***")
            result = f(self)
            save_print_dbg(f"Finished '{self.feature}'")
            self.run_time += (datetime.now() - self.start_time).seconds
            minutes = int(self.run_time / 60)
            txt = '_____Total %s:%ss' % (minutes, self.run_time - 60 * minutes)
            save_print_dbg(txt=txt)
            save_print_dbg(f"***Finished '{self.name}***'")
            return result
        return wrapper

    def decorator_save_result(fun):
        def wrapper(self):
            self.result = fun(self)
            self._save_result(self.result)

        return wrapper

    def _save_result(self, result: bool):
        marker = get_json_file(USAGE_FILE)

        # mapping
        if self.feature not in marker:
            marker[self.feature] = {
                'total_time': self.run_time,
                'total_run': 1,
                'runnable': result
            }
        else:
            marker[self.feature]['total_time'] += self.run_time
            marker[self.feature]['total_run'] += 1
            marker[self.feature]['runnable'] = result
        marker['last_run_at'] = datetime.strftime(
            datetime.now(), READABLE_TIME_FORMAT)

        save_json_file(USAGE_FILE, marker, is_sort=True)

    def decorator_ignore_warning(f):
        def wrapper(self):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return f(self)
        return wrapper

    @decorator_ignore_warning
    @decorator_save_result
    @if_auto_run_then_wait_town
    @decorator_init
    @go_main_screen
    @decorator_catch_exceptions
    def _run(self):
        '''
        This call self.select_run, since it will be extended
        Use self.start/1 to run
        '''
        const.dbg_name = f'{self.name}'
        self.check_smart_rerun_energy()
        self.total_selected_cost += 1
        self.select_run()
        self.main_run()
        while self.rerun_mode:
            sleep(3 * SECOND)
            self.main_run()

    def select_run(self):
        '''
        Inherit class will extend this function to setup for run
        E.g. select mode, select cost
        To keep the decorator in self._run
        '''
        pass

    @sleep_decorator
    def main_run(self):
        '''
        Inherit class will extend this function to run test
        This separate function for rerun_mode
        '''
        pass

    def _start_thread(self):
        '''
        Create a thread to run farm
        Due to failed to use Process with depth decorator and function
        so using Process to create a Thread, so when we need to stop a process farming
        we can use Process.terminate (it will kill there child)
        Using self.start instead
        '''
        self.thread = threading.Thread(target=self._run, args=())
        self.thread.start()

    def start(self, wait_done=False):
        if self.thread:
            return

        self.start_time = datetime.now()
        self.process = multiprocessing.Process(target=self._start_thread)
        self.process.start()

        if wait_done:
            self.process.join()

    def stop(self):
        if self.process:
            self.process.terminate()
        # self.thread = None
        # self.process = None
        # mark farm as runnable, do due this terminated
        self.run_time = (datetime.now() - self.start_time).seconds
        self._save_result(True)

    def is_done(self) -> bool:
        if self.process:
            return not self.process.is_alive()
        return False

    def wait_done(self):
        if self.process:
            self.process.join()

    def get_config(self):
        cfg = get_json_file(CONFIG_FILE)
        self.cfg = cfg.get(self.feature, {})
        self.decline_treasure = cfg.get('decline_treasure', True)
        self.rerun_mode = cfg.get('rerun_mode', False)
        self.smart_rerun_energy = cfg.get('smart_rerun_energy', False)

    def mapping_config(self):
        if not self.cfg:
            self.cfg = {}

    def validate(self):
        if not self.feature:
            raise InvalidValueValidateException(
                farm='', key='feature',
                value=self.feature, expect='!=null')
        if type(self.decline_treasure) != bool:
            raise InvalidValueValidateException(
                farm='', key='decline_treasure',
                value=self.decline_treasure, expect='not boolean')
        if type(self.smart_rerun_energy) != bool:
            raise InvalidValueValidateException(
                farm='', key='smart_rerun_energy',
                value=self.smart_rerun_energy, expect='not boolean')

    def get_run_time(self) -> int:
        if self.is_done():
            return self.run_time
        return (datetime.now() - self.start_time).seconds

    def get_result(self) -> bool:
        return get_json_file(USAGE_FILE).get(self.feature, {}).get('runnable', False)

    def show_config_ui(self, parent, main):
        if self.configUI != None:
            self.configUI(self, parent, main)

    def check_smart_rerun_energy(self):
        if not self.is_valid_smart_rerun_energy():
            return
        self.cost = max(max(LIST_COSTS) -
                        self.total_selected_cost, min(LIST_COSTS))

    def is_smart_rerun_energy(self) -> bool:
        if not self.is_valid_smart_rerun_energy():
            return
        return not (self.cost == min(LIST_COSTS))

    def is_valid_smart_rerun_energy(self) -> bool:
        return hasattr(self, 'cost') and self.smart_rerun_energy and is_rerun_mode()

    def __str__(self) -> str:
        return '\n'.join([f"Farm: {self.feature}\tRerun: {self.rerun_mode}"])
