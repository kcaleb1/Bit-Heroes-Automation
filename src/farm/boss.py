from utils import check_no_energy, click_town, enable_auto_on, find_image, find_image_and_click_then_sleep, run_or_raise_exception, sleep
from window import press_escape
from const import *
from error import *
from decorator import feature, go_main_screen, farm_exceptions, is_run
from datetime import datetime


FEATURE_PATH = join(IMG_PATH, 'boss')
BTN = join(FEATURE_PATH, 'button.png')
FULL_TXT = join(FEATURE_PATH, 'full.png')
JOIN_BTN = join(FEATURE_PATH, 'join.png')
READY_BTN = join(FEATURE_PATH, 'ready.png')
START_BTN = join(FEATURE_PATH, 'start.png')


@feature('boss')
@is_run
@farm_exceptions
def go_boss(is_loop=True, **kwargs):
    run_boss(**kwargs)
    while is_loop:
        run_boss(**kwargs)


@go_main_screen
def run_boss(**kwargs):
    find_image_and_click_then_sleep(BTN)
    try:
        find_image_and_click_then_sleep(
            JOIN_BTN, retry_time=3, sleep_duration=1)
    except:
        return run_boss(**kwargs)

    check_no_energy()

    try:
        find_image(COMMON_CLOSE, retry_time=3)
        return run_boss(**kwargs)
    except:
        pass

    find_image_and_click_then_sleep(READY_BTN)
    start_time = datetime.now()
    is_started = False
    is_auto_on = False
    is_pressed_escape = False
    while True:
        is_started = click_town()
        if is_started:
            break

        if not is_auto_on:
            # check got kicked from room
            try:
                find_image_and_click_then_sleep(COMMON_CLOSE, retry_time=1)
                return run_boss(**kwargs)
            except:
                pass

            # check when become host, leave lobby and rerun
            try:
                find_image(START_BTN, retry_time=1)
                return run_boss(**kwargs)
            except:
                pass

            is_auto_on = enable_auto_on()

        # this will help to exit the lobby when host afk to long
        # press escape, in case of already in-game, this will turn off auto play
        # and the click COMMON_AUTO_OFF will handle it
        if not is_auto_on and (datetime.now() - start_time).seconds >= 60:
            if is_pressed_escape:
                break
            press_escape()
            is_pressed_escape = True

    if not is_started:
        sleep(0.5)
        find_image_and_click_then_sleep(COMMON_YES)
        return run_boss(**kwargs)
