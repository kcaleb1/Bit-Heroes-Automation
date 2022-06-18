from time import sleep
from utils import \
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


def create_usage_file(fun):
    def wrapper(*args, **kwargs):
        # if file not exist, or failed load, create empty file
        try:
            get_json_file(USAGE_FILE)
        except:
            save_json_file(USAGE_FILE, {})
        return fun(*args, **kwargs)
    return wrapper
