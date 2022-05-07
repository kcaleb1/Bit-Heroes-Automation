from random import uniform
from time import sleep

from utils import find_image_and_click_then_sleep, find_image, go_main_screen, run_or_raise_exception
from window import click_screen_and_sleep
from const import *
from error import *

IMAGE_PATH = join(CUR_PATH, 'img', 'fishing')
BTN = join(IMAGE_PATH, 'button.png')
PLAY_BTN = join(IMAGE_PATH, 'play.png')
START_BTN = join(IMAGE_PATH, 'start.png')
CAST_BTN = join(IMAGE_PATH, 'cast.png')
CATCH_BTN = join(IMAGE_PATH, 'catch.png')
TRADE_BTN = join(IMAGE_PATH, 'trade.png')
CLOSE_BTN = join(IMAGE_PATH, 'close.png')
EMPTY_BAIT = join(IMAGE_PATH, 'empty-bait.png')
PERCENT_100 = join(IMAGE_PATH, '100-percent.png')


def go_fishing(is_loop=False):
    go_main_screen()

    try:
        find_image_and_click_then_sleep(BTN)
        find_image_and_click_then_sleep(PLAY_BTN)
        sleep(SLEEP*10)  # wait for walking
        doing_fish(initial=True)
        while is_loop:
            doing_fish()
    except EmptyBaitException as ex:
        print(ex.__str__())
    except KeyboardInterrupt as ex:
        raise ex
    except Exception as ex:
        print('got error when go_fishing: ', ex)


def doing_fish(initial=False):
    def is_check_closes() -> bool:
        try:
            find_image_and_click_then_sleep(
                CLOSE_BTN, retry_time=1, sleep_duration=0.5)
            find_image_and_click_then_sleep(COMMON_SMALL_X_BTN, retry_time=1)
            return True
        except:
            return False

    run_or_raise_exception(
        lambda: find_image(EMPTY_BAIT, threshold=0.9,
                           retry_time=10 if initial else 5),
        EmptyBaitException
    )

    y_start, x_start = find_image(START_BTN)
    # click start
    click_screen_and_sleep(y_start, x_start, uniform(0, 0.5))
    # click cast
    click_screen_and_sleep(y_start, x_start, sleep_duration=SLEEP * 7)
    # when got trash
    try:
        find_image_and_click_then_sleep(TRADE_BTN)
        return  # stop when got trash
    except:
        pass

    while True:
        try:
            find_image(PERCENT_100, retry_time=1, threshold=0.5)
            break
        except:
            pass

        if is_check_closes():
            return

    # click catch
    click_screen_and_sleep(y_start, x_start, sleep_duration=SLEEP * 15)

    try:
        find_image_and_click_then_sleep(TRADE_BTN, sleep_duration=SLEEP)
    except:
        pass

    for _ in range(5):
        if is_check_closes():
            return

        try:
            find_image_and_click_then_sleep(COMMON_SMALL_X_BTN, retry_time=1)
            return
        except:
            pass
