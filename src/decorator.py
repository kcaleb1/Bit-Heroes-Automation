import json
from utils import go_main_screen as do_go_main_screen
from const import USAGE_FILE


def go_main_screen(f):
    def wrapper(*args, **kwargs):
        do_go_main_screen()
        return f(*args, **kwargs)
    return wrapper


def create_USAGE_FILE(fun):
    def wrapper(*args, **kwargs):
        # if file not exist, or failed load, create empty file
        try:
            with open(USAGE_FILE, 'r') as f:
                json.load(f)
        except:
            with open(USAGE_FILE, 'w') as f:
                f.write(json.dumps({}, indent=4))
        return fun(*args, **kwargs)
    return wrapper
