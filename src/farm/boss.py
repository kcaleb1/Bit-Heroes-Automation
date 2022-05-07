from utils import find_image_and_click_then_sleep
from utils import go_main_screen
from const import *
from error import *


IMAGE_PATH = join(CUR_PATH, 'img', 'boss')
BTN = join(IMAGE_PATH, 'button.png')


def go_boss(is_loop=False):
    go_main_screen()

    raise UnimplementedException()

    try:
        find_image_and_click_then_sleep(BTN)
    except Exception as e:
        print('got error when go_boss: ', e)
