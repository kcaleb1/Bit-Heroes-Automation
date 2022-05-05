from random import uniform
from time import sleep

from utils import find_image_and_click_then_sleep, find_image, go_main_screen
from window import click_screen_and_sleep
from const import *
from error import *


def go_fishing(is_loop=False):
    go_main_screen()

    try:
        find_image_and_click_then_sleep(FISHING_BTN)
        find_image_and_click_then_sleep(FISHING_PLAY_BTN)
        sleep(SLEEP*10) # wait for walking
        doing_fish()
        while is_loop:
            doing_fish()
    except EmptyBaitException as err:
        print(err.__str__())
    except Exception as e:
        print('got error when go_fishing: ', e)

def doing_fish():
    try:
        find_image(FISHING_EMPTY_BAIT, threshold=0.9)
        raise EmptyBaitException()
    except EmptyBaitException as ex:
        raise ex
    except:
        pass

    y_start, x_start = find_image(FISHING_START_BTN)
    # click start
    click_screen_and_sleep(y_start, x_start, uniform(0, 0.5))
    # click cast
    click_screen_and_sleep(y_start, x_start, sleep_duration=SLEEP * 7)
    # when got trash
    try:
        find_image_and_click_then_sleep(FISHING_TRADE_BTN)
        return # stop when got trash
    except:
        pass

    find_image(FISHING_100_PERCENT, retry_time=50, threshold=0.5)
    # click catch
    click_screen_and_sleep(y_start, x_start, sleep_duration=SLEEP * 15)

    try: find_image_and_click_then_sleep(FISHING_TRADE_BTN, sleep_duration=SLEEP * 5)
    except: pass

    try: find_image_and_click_then_sleep(FISHING_CLOSE_BTN, retry_time=5)
    except:
        pass
    
    try: find_image_and_click_then_sleep(COMMON_SMALL_X_BTN)
    except: pass
