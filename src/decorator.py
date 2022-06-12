from time import sleep
from utils import click_town_or_rerun, \
    enable_auto_on, \
    get_json_file, \
    go_main_screen as do_go_main_screen, \
    save_json_file
from const import SLEEP, USAGE_FILE


def go_main_screen(f):
    def wrapper(*args, **kwargs):
        do_go_main_screen()
        return f(*args, **kwargs)
    return wrapper


def sleep_decorator(f):
    def wrapper(*args, **kwargs):
        sleep(1.5)
        return f(*args, **kwargs)
    return wrapper


def if_auto_run_then_wait_town(f):
    '''
    Use to check if farm start while other farm running
    then wait and go town, to start
    '''
    def wrapper(*args, **kwargs):
        for _ in range(5):
            t = enable_auto_on()
            if t:
                while not click_town_or_rerun():
                    sleep(SLEEP)
                break
        else:
            click_town_or_rerun()
        return f(*args, **kwargs)
    return wrapper


def create_usage_file(fun):
    def wrapper(*args, **kwargs):
        # if file not exist, or failed load, create empty file
        try:
            get_json_file(USAGE_FILE)
        except:
            save_json_file(USAGE_FILE, {})
        return fun(*args, **kwargs)
    return wrapper
