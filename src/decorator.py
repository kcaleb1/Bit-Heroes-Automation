import json
from error import UnableJoinBossException, EmptyBaitException, MismatchConditionException, UnimplementedException, NoEnergyException
from utils import find_image_and_click_then_sleep, go_main_screen as do_go_main_screen
from window import get_app, get_game_screen
from datetime import datetime
from debug import save_print_dbg
from const import MARKER_FILE, TIME_FORMAT, cfg, COMMON_RECONNECT
import const


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
        find_image_and_click_then_sleep(
            COMMON_RECONNECT, retry_time=10, sleep_duration=0.5, ignore_exception=True)
        const.dbg_name = old_name
        return f(*args, **kwargs)
    return wrapper


def create_marker_file(fun):
    def wrapper(*args, **kwargs):
        try:
            with open(MARKER_FILE, 'r') as f:
                json.load(f)
        except:
            with open(MARKER_FILE, 'w') as f:
                f.write(json.dumps({}, indent=4))
        return fun(*args, **kwargs)
    return wrapper
