from error import EmptyBaitException, MismatchConditionException, UnimplementedException, NoEnergyException
from utils import go_main_screen as do_go_main_screen
from window import get_app, get_game_screen
from datetime import datetime
from debug import save_print_dbg
from const import TIME_FORMAT, cfg
import const


def unimplemented(f):
    def wrapper(*args, **kwargs):
        print(UnimplementedException(kwargs['feature']).__str__())
        return
    return wrapper


def feature(feature: str):
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


def farm_exceptions(f):
    def wrapper(*args, **kwargs):
        err = ''
        try:
            return f(*args, **kwargs)
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


def is_run(f):
    def wrapper(*args, **kwargs):
        if kwargs.get('cfg', {}).get('is_run', False):
            return f(*args, **kwargs)
        else:
            txt = f"Feature '{kwargs.get('feature')}' disabled"
            print(txt)
            save_print_dbg(txt=txt, is_print=False)
    return wrapper


def time_messure(f):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        r = f(*args, **kwargs)
        seconds = (datetime.now() - start).seconds
        minutes = int(seconds / 60)
        print('Total %s:%ss' % (minutes, seconds - 60 * minutes))
        return r
    return wrapper