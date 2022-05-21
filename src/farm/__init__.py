from datetime import datetime
from json import load
import json
import multiprocessing
import threading
import warnings
from const import CONFIG_FILE, MARKER_FILE, TIME_FORMAT
import const
from debug import save_print_dbg
from decorator import go_main_screen
from error import EmptyBaitException, InvalidValueValidateException, NoEnergyException, UnableJoinBossException


class Farm(object):
    feature = None
    name = None
    thread = None
    process = None
    is_run = False
    debug = None
    run_time = 0

    def __init__(self, feature: str):
        self.feature = feature
        self.reset_config()

    def hard_reset_config(self):
        self.reset_config()
        self.thread = None

    def reset_config(self):
        self.run_time = 0
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
                err = NoEnergyException(feature=str(self.feature))
            except KeyboardInterrupt:
                err = f"'{self.feature}' stopped by keyboard"
            except EmptyBaitException as ex:
                err = str(ex)
            except UnableJoinBossException as ex:
                err = str(ex)
                special = True
            except Exception as ex:
                err = f"got error when run '{self.feature}': {str(ex)}"
            print(err)
            save_print_dbg(txt=err, is_print=False)
            return True if special else False
        return wrapper

    def decorator_init(f):
        def wrapper(self):
            start = datetime.now()
            print(f"Running '{self.feature}'")
            save_print_dbg(f"\n***Debug for '{self.name}'***")
            result = f(self)
            print(f"Finished '{self.feature}'")
            self.run_time += (datetime.now() - start).seconds
            minutes = int(self.run_time / 60)
            txt = '_____Total %s:%ss' % (minutes, self.run_time - 60 * minutes)
            print(txt)
            save_print_dbg(txt=txt, is_print=False)
            save_print_dbg(f"***Finished '{self.name}***'")
            return result
        return wrapper

    def decorator_save_result(fun):
        def wrapper(self):
            self.result = fun(self)
            marker = {}
            with open(MARKER_FILE, 'r') as f:
                marker = json.load(f)
            # mapping
            if self.feature not in marker:
                marker[self.feature] = {
                    'total_time': self.run_time,
                    'total_run': 1,
                    'runnable': self.result
                }
            else:
                marker[self.feature]['total_time'] += self.run_time
                marker[self.feature]['total_run'] += 1
                marker[self.feature]['runnable'] = self.result

            # store to marker.json
            with open(MARKER_FILE, 'w') as f:
                f.write(json.dumps(marker, indent=4, sort_keys=True))
        return wrapper

    def decorator_ignore_warning(f):
        def wrapper(self):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return f(self)
        return wrapper

    @decorator_ignore_warning
    @decorator_save_result
    @decorator_init
    @go_main_screen
    @decorator_catch_exceptions
    def _run(self):
        '''
        This call self.do_run, since it will be extended
        Use self.start/1 to run
        '''
        const.dbg_name = f'{self.name}'
        self.start_time = datetime.now()
        self.do_run()

    def do_run(self):
        '''
        Inherit class will extend this function to run test
        To keep the decorator in self._run
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

        self.process = multiprocessing.Process(target=self._start_thread)
        self.process.start()

        if wait_done:
            self.process.join()

    def stop(self):
        if self.process:
            self.process.terminate()
        self.thread = None
        self.process = None

    def is_done(self):
        if self.process:
            return not self.process.is_alive()
        return False

    def wait_done(self):
        if self.process:
            self.process.join()

    def get_config(self):
        with open(CONFIG_FILE, 'r') as f:
            self.cfg = load(f).get(self.feature, {})

    def mapping_config(self):
        if not self.cfg:
            self.cfg = {}
        self.is_run = self.cfg.get('is_run', False)

    def validate(self):
        if not self.feature:
            raise InvalidValueValidateException(
                key='feature', value=self.feature, expect='!=null')

    def get_result(self):
        with open(MARKER_FILE, 'r') as f:
            return json.load(f).get(self.feature, {}).get('runnable', False)

    def __str__(self) -> str:
        return f"Farm: {self.feature}\n"
