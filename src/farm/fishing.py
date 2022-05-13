from random import uniform
from decorator import feature, go_main_screen, farm_exceptions, is_run

from utils import find_image_and_click_then_sleep, find_image, run_or_raise_exception, sleep
from window import click_screen_and_sleep
from const import *
from error import *

FEATURE_PATH = join(IMG_PATH, 'fishing')
BTN = join(FEATURE_PATH, 'button.png')
START_BTN = join(FEATURE_PATH, 'start.png')
CAST_BTN = join(FEATURE_PATH, 'cast.png')
CATCH_BTN = join(FEATURE_PATH, 'catch.png')
TRADE_BTN = join(FEATURE_PATH, 'trade.png')
EMPTY_BAIT = join(FEATURE_PATH, 'empty-bait.png')
PERCENT_100 = join(FEATURE_PATH, '100-percent.png')


@feature('fishing')
@is_run
@go_main_screen
@farm_exceptions
def go_fishing(is_loop=True, **kwargs):
    find_image_and_click_then_sleep(BTN)
    find_image_and_click_then_sleep(COMMON_PLAY)
    doing_fish(initial=True)
    while is_loop:
        doing_fish()


def doing_fish(initial=False):
    def is_check_closes() -> bool:
        try:
            find_image_and_click_then_sleep(
                COMMON_CLOSE, retry_time=1, sleep_duration=0.5, threshold=0.9)
            find_image_and_click_then_sleep(COMMON_SMALL_X, retry_time=1, threshold=0.9)
            return True
        except:
            return False

    y_start, x_start = 0, 0
    while True:
        try:
            y_start, x_start = find_image(START_BTN)
            break
        except:
            pass
        
    # click start
    click_screen_and_sleep(y_start, x_start, uniform(0, 0.5))
    # click cast
    click_screen_and_sleep(y_start, x_start)
    sleep(4)
    # when got trash
    try:
        find_image_and_click_then_sleep(TRADE_BTN, sleep_duration=0.5, retry_time=3)
        find_image_and_click_then_sleep(COMMON_SMALL_X, threshold=0.9, retry_time=3)
        return  # stop when got trash
    except:
        pass
    
    run_or_raise_exception(
        lambda: find_image(START_BTN, retry_time=3),
        EmptyBaitException
    )

    while True:
        try:
            find_image(PERCENT_100, retry_time=20, threshold=0.5, find_interval=0.2)
            break
        except:
            pass

        if is_check_closes():
            return

    # click catch
    click_screen_and_sleep(y_start, x_start, sleep_duration=3)
    find_image_and_click_then_sleep(TRADE_BTN, ignore_exception=True)

    for _ in range(10):
        if is_check_closes():
            return

        try:
            find_image_and_click_then_sleep(COMMON_SMALL_X, retry_time=1)
            return
        except:
            pass
