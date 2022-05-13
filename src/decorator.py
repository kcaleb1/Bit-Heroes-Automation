from error import EmptyBaitException, MismatchConditionException, UnimplementedException, NoEnergyException
from utils import find_image_and_click_then_sleep, go_main_screen as do_go_main_screen
from window import get_app, get_game_screen
from datetime import datetime
from debug import save_print_dbg
from const import TIME_FORMAT, cfg, COMMON_RECONNECT
import const
from time import sleep


def unimplemented(f):
    def wrapper(*args, **kwargs):
        print(UnimplementedException(kwargs['feature']).__str__())
        return
    return wrapper


def feature(feature: str) -> bool:
    def decorator(f):
        def wrapper(*args, **kwargs):
            kwargs['feature'] = feature
            kwargs['cfg'] = cfg[feature]
            rename = feature.replace(' ', '_')
            const.dbg_name = datetime.now().strftime(f'{TIME_FORMAT}_{rename}')
            print(f"Running '{feature}'")
            save_print_dbg(f"\n***Debug for '{const.dbg_name}'***")
            result = f(*args, **kwargs)
            print(f"Finished '{feature}'")
            save_print_dbg(f"***Finished '{const.dbg_name}***'")
            return result
        return wrapper
    return decorator


def go_main_screen(f):
    def wrapper(*args, **kwargs):
        do_go_main_screen()
        return f(*args, **kwargs)
    return wrapper


def go_main_screen_after(f):
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
        do_go_main_screen()
    return wrapper


def farm_exceptions(f) -> bool:
    def wrapper(*args, **kwargs):
        err = ''
        try:
            f(*args, **kwargs)
            return True
        except NoEnergyException:
            err = NoEnergyException(feature=kwargs['feature']).__str__()
        except KeyboardInterrupt:
            err = f"'{kwargs['feature']}' stopped by keyboard".__str__()
        except EmptyBaitException as ex:
            err = ex.__str__()
        except Exception as ex:
            err = f"got error when run '{kwargs['feature']}': {ex.__str__()}"
        print(err)
        save_print_dbg(txt=err, is_print=False)
        return False
    return wrapper


def focus_game(f):
    def wrapper(*args, **kwargs):
        print('Checking precondition')
        ex = None
        try:
            get_app()
            get_game_screen()
        except MismatchConditionException as e:
            ex = e.__str__()
        except:
            ex = MismatchConditionException(txt='Game not found').__str__()
        if ex:
            print(ex)
            save_print_dbg(txt=ex, is_print=False)
            return
        print('We are good to go...')
        return f(*args, **kwargs)
    return wrapper


def terminal_wait(f):
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
        input('Press enter to close...')
    return wrapper


def is_run(f) -> bool:
    def wrapper(*args, **kwargs):
        if kwargs.get('cfg', {}).get('is_run', False):
            return f(*args, **kwargs)
        else:
            txt = f"Feature '{kwargs.get('feature')}' disabled"
            print(txt)
            save_print_dbg(txt=txt, is_print=False)
            return False
    return wrapper


def time_messure(f):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        r = f(*args, **kwargs)
        seconds = (datetime.now() - start).seconds
        minutes = int(seconds / 60)
        txt = '_____Total %s:%ss' % (minutes, seconds - 60 * minutes)
        print(txt)
        save_print_dbg(txt=txt, is_print=False)
        return r
    return wrapper


def check_reconnect(f):
    def wrapper(*args, **kwargs):
        old_name = const.dbg_name
        const.dbg_name = datetime.now().strftime(f'{TIME_FORMAT}_reconnect')
        try:
            find_image_and_click_then_sleep(COMMON_RECONNECT, retry_time=10, sleep_duration=0.5)
        except:
            pass
        const.dbg_name = old_name
        return f(*args, **kwargs)
    return wrapper