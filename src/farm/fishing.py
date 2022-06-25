from random import uniform
from farm import Farm
from utils import find_image_and_click_then_sleep, find_image, raise_exception_when_runnable, sleep
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


class Fishing(Farm):
    feature = 'fishing'

    def __init__(self):
        super().__init__()
        self.button = BTN
        self.no_energy_bars = []

    def is_check_closes(self):
        try:
            find_image_and_click_then_sleep(
                COMMON_CLOSE, retry_time=1, sleep_duration=0.5, threshold=0.9)
            find_image_and_click_then_sleep(
                COMMON_SMALL_X, retry_time=1, threshold=0.9)
            return True
        except:
            return False

    def config_run(self):
        super().config_run()
        find_image_and_click_then_sleep(COMMON_PLAY)

    # TODO optimize this
    def main_run(self):
        y_start, x_start = 0, 0
        while True:
            try:
                y_start, x_start = find_image(START_BTN)
                break
            except:
                pass

        # click start
        click_screen_and_sleep(y_start, x_start, uniform(0.5, 1.5))
        # click cast
        click_screen_and_sleep(y_start, x_start)
        sleep(4)
        # when got trash
        try:
            find_image_and_click_then_sleep(
                TRADE_BTN, sleep_duration=0.5, retry_time=3)
            find_image_and_click_then_sleep(
                COMMON_SMALL_X, threshold=0.9, retry_time=3)
            return  # stop when got trash
        except:
            pass

        raise_exception_when_runnable(
            lambda: find_image(START_BTN, retry_time=3),
            EmptyBaitException
        )

        while True:
            try:
                find_image(PERCENT_100, retry_time=20,
                           threshold=0.6, find_interval=0.2)
                break
            except:
                pass

            if self.is_check_closes():
                return

        # click catch
        click_screen_and_sleep(y_start, x_start, sleep_duration=3)
        find_image_and_click_then_sleep(TRADE_BTN, ignore_exception=True)

        for _ in range(6):
            if self.is_check_closes():
                return

            try:
                find_image_and_click_then_sleep(COMMON_SMALL_X, retry_time=1)
                return
            except:
                pass
