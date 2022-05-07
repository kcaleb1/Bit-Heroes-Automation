from time import sleep
from decorator import feature, go_main_screen, farm_exceptions
from utils import find_image_and_click_then_sleep, find_image, run_or_raise_exception
from window import click_screen_and_sleep
from const import *
from error import *


FEATURE_PATH = join(IMG_PATH, 'raid')
BTN = join(FEATURE_PATH, 'button.png')
MOVE_LEFT_BTN = join(FEATURE_PATH, 'move-left.png')
SUMMON_BTN = join(FEATURE_PATH, 'summon.png')
NO_ENERGY = join(FEATURE_PATH, 'no-energy.png')

BOSSES = {
    1: join(FEATURE_PATH, 'boss-1.png'),
    2: join(FEATURE_PATH, 'boss-2.png'),
    3: join(FEATURE_PATH, 'boss-3.png'),
    4: join(FEATURE_PATH, 'boss-4.png')
}


@feature('farm raid')
@go_main_screen
@farm_exceptions
def go_raid(is_loop=False, boss=1, difficulty=1, **kwargs):
    find_image_and_click_then_sleep(BTN)

    run_or_raise_exception(
        lambda: find_image(NO_ENERGY, threshold=0.9),
        NoEnergyException
    )

    while True:
        try:
            find_image(BOSSES[boss], retry_time=1)
            break
        except:
            find_image_and_click_then_sleep(MOVE_LEFT_BTN)
            sleep(0.5)

    find_image_and_click_then_sleep(SUMMON_BTN)
    find_image_and_click_then_sleep(DIFFICULTIES[difficulty])

    find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
    find_image_and_click_then_sleep(COMMON_ACCEPT)

    do_raid()
    while is_loop:
        do_raid()


def do_raid():
    run_or_raise_exception(
        lambda: find_image_and_click_then_sleep(COMMON_NO_BTN, threshold=0.9, retry_time=20),
        NoEnergyException
    )

    while True:
        try:
            find_image(COMMON_AUTO_ON)
            break
        except:
            try:
                find_image_and_click_then_sleep(COMMON_AUTO_OFF)
            except:
                pass
            break

    while True:
        try:
            y, x = find_image(COMMON_RERUN)
            sleep(1)
            click_screen_and_sleep(y, x)
            break
        except:
            pass
