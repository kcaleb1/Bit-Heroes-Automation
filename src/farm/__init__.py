from datetime import datetime
import multiprocessing
import threading
from time import sleep
import warnings
from const import COMMON_NO_ENERGY_BAR_1, COMMON_NO_ENERGY_BAR_2, CONFIG_FILE, LIST_COSTS, READABLE_TIME_FORMAT, SECOND, SLEEP, USAGE_FILE, TIME_FORMAT
import const
from debug import save_print_dbg
from decorator import go_main_screen, sleep_decorator
from error import EmptyBaitException, InvalidValueValidateException, MismatchConditionException, NoEnergyException, UnableJoinException
from window import get_app
from utils import \
    click_town_or_rerun, \
    enable_auto_on, \
    find_image_and_click_then_sleep, \
    get_json_file, \
    is_image_exist, \
    is_no_energy_bar, \
    is_rerun_mode, \
    save_json_file


class Farm(object):
    feature = None
    button = None
    configUI = None
    name = None
    thread = None
    process = None
    debug = None
    run_time = 0
    no_energy_bars = [COMMON_NO_ENERGY_BAR_1, COMMON_NO_ENERGY_BAR_2]
    default_config = {}

    def __init__(self):
        self.reset_config()

    def hard_reset_config(self):
        self.reset_config()
        self.thread = None

    def reset_config(self):
        self.run_time = 0
        self.total_selected_cost = 0
        self.start_time = None
        self.flag_brush_force_energy = False
        self.save_status('Waiting to start...')
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
                if self.is_brush_force_energy():
                    # in case of smart rerun enabled
                    if not self.rerun_mode:
                        special = True
                    else:
                        self.flag_brush_force_energy = True
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

    def decorator_if_auto_run_then_wait_town(f):
        '''
        Use to check if farm start while other farm running
        then wait and go town, to start
        '''

        def wrapper(self):
            if not is_image_exist(self.button):
                self.save_status('Check reconnect or running...')
                for _ in range(4):
                    if enable_auto_on():
                        while not click_town_or_rerun():
                            sleep(SLEEP)
                        break
                else:
                    click_town_or_rerun()
            return f(self)
        return wrapper

    def _save_result(self, result: bool):
        usage = get_json_file(USAGE_FILE)

        # mapping
        if self.feature not in usage:
            usage[self.feature] = {
                'total_time': self.run_time,
                'total_run': 1,
                'runnable': result
            }
        else:
            validate = {
                'total_time': 0,
                'total_run': 0,
            }
            for k, v in validate.items():
                if k not in usage[self.feature]:
                    usage[self.feature][k] = v

            usage[self.feature]['total_time'] += self.run_time
            usage[self.feature]['total_run'] += 1
            usage[self.feature]['runnable'] = result
        usage['last_run_at'] = datetime.strftime(
            datetime.now(), READABLE_TIME_FORMAT)

        save_json_file(USAGE_FILE, usage, is_sort=True)

    def decorator_ignore_warning(f):
        def wrapper(self):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return f(self)
        return wrapper

    @decorator_ignore_warning
    @decorator_save_result
    @decorator_if_auto_run_then_wait_town
    @decorator_init
    @go_main_screen
    @decorator_catch_exceptions
    def _run(self):
        '''
        This call self.config_run, since it will be extended
        Use self.start/1 to run
        '''
        const.dbg_name = f'{self.name}'

        self.check_brush_force_energy()
        self.total_selected_cost += 1
        self.save_cost_to_usage()

        self.save_status('Selecting mode...')
        self.select_mode()
        if is_no_energy_bar(self.no_energy_bars):
            self.flag_brush_force_energy = False
            raise NoEnergyException()
        self.config_run()
        self.save_status('Running...')
        self.main_run()
        while self.rerun_mode:
            sleep(3 * SECOND)
            self.main_run()

    def select_mode(self):
        if not self.button:
            raise MismatchConditionException(txt='Missing button image')
        # when rerun with smart energy, don't need to click mode again
        if self.flag_brush_force_energy:
            return
        find_image_and_click_then_sleep(self.button, retry_time=3)

    def config_run(self):
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
        self.save_error('')

        if wait_done:
            self.process.join()

    def stop(self):
        self.save_status('Stopped...')
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
        self.brush_force_energy = cfg.get('brush_force_energy', False)

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
        if type(self.brush_force_energy) != bool:
            raise InvalidValueValidateException(
                farm='', key='brush_force_energy',
                value=self.brush_force_energy, expect='not boolean')

    def get_run_time(self) -> int:
        if self.is_done():
            return self.run_time
        return (datetime.now() - self.start_time).seconds

    def get_result(self) -> bool:
        return get_json_file(USAGE_FILE).get(self.feature, {}).get('runnable', False)

    def show_config_ui(self, parent, main):
        if self.configUI != None:
            self.configUI(self, parent, main)

    def check_brush_force_energy(self):
        if not self.is_valid_brush_force_energy():
            return
        cost = max(max(LIST_COSTS) -
                   self.total_selected_cost, min(LIST_COSTS))
        save_print_dbg(f'Change cost from {self.cost} to {cost}')
        self.cost = cost

    def is_brush_force_energy(self) -> bool:
        if not self.is_valid_brush_force_energy():
            return False
        return not (self.cost == min(LIST_COSTS))

    def is_valid_brush_force_energy(self) -> bool:
        return hasattr(self, 'cost') and self.brush_force_energy == True and is_rerun_mode()

    def save_cost_to_usage(self):
        if not hasattr(self, 'cost'):
            return
        usage = get_json_file(USAGE_FILE)
        usage[self.feature]['cost'] = self.cost
        save_json_file(USAGE_FILE, usage)

    def get_cost_from_usage(self) -> int:
        if not hasattr(self, 'cost'):
            return -1

        return get_json_file(USAGE_FILE).get(self.feature, {}).get('cost', self.cost)

    def save_status(self, status: str):
        usage = get_json_file(USAGE_FILE)
        usage['status'] = status
        save_json_file(USAGE_FILE, usage)

    def get_status_from_usage(self) -> str:
        return get_json_file(USAGE_FILE).get('status', 'None')

    def save_error(self, error: str):
        '''
        Use when got error that can't re-run able
        e.g. Tier raid/quest unreachable
        '''
        usage = get_json_file(USAGE_FILE)
        f = usage.get(self.feature, {})
        f['error'] = error
        usage[self.feature] = f
        save_json_file(USAGE_FILE, usage)

    def get_error(self) -> str:
        return get_json_file(USAGE_FILE).get(self.feature, {}).get('error', '')

    def __str__(self) -> str:
        txt = [f"Farm: {self.feature}\tRerun: {self.rerun_mode}"]
        return '\n'.join([self.get_status_from_usage()] + txt)

    def set_default_config(self):
        '''
        When got error related to config, UI will call this function to reset config to default
        Set default config into self.default_config
        '''
        cfg = get_json_file(CONFIG_FILE)
        cfg[self.feature] = self.default_config
        save_json_file(CONFIG_FILE, cfg)
