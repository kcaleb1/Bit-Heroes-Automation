from utils import find_image, find_image_and_click_then_sleep, run_or_raise_exception, sleep
from window import click_screen_and_sleep, press_escape
from const import *
from error import *
from decorator import feature, go_main_screen, farm_exceptions, is_run
from datetime import datetime


FEATURE_PATH = join(IMG_PATH, 'boss')
BTN = join(FEATURE_PATH, 'button.png')
FULL_TXT = join(FEATURE_PATH, 'full.png')
JOIN_BTN = join(FEATURE_PATH, 'join.png')
READY_BTN = join(FEATURE_PATH, 'ready.png')


@feature('boss')
@is_run
@go_main_screen
@farm_exceptions
def go_boss(is_loop=True, **kwargs):
    find_image_and_click_then_sleep(BTN)
    run_boss(**kwargs)
    while is_loop:
        run_boss(**kwargs)

def run_boss(**kwargs):    
    try:
        find_image_and_click_then_sleep(JOIN_BTN)
    except:
        return run_boss(**kwargs)
    
    run_or_raise_exception(
        lambda: find_image(COMMON_NO, retry_time=3, threshold=0.9),
        NoEnergyException
    )
    
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
        try:
            y, x = find_image(COMMON_TOWN, retry_time=1)
            sleep(1)
            click_screen_and_sleep(y, x)
            is_started = True
            break
        except:
            pass

        if not is_auto_on:
            try:
                find_image(COMMON_AUTO_ON, retry_time=1, threshold=0.9)
                is_auto_on = True
                continue
            except:
                pass

            try:
                find_image_and_click_then_sleep(COMMON_AUTO_OFF, retry_time=1)
                is_auto_on = True
            except:
                pass

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
