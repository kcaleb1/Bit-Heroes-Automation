from decorator import farm_exceptions, feature, go_main_screen
from const import *
from error import NoEnergyException
from utils import find_image, find_image_and_click_then_sleep, run_or_raise_exception, sleep
from window import click_screen_and_sleep, press_escape

FEATURE_PATH = join(IMG_PATH, 'pvp')
BTN = join(FEATURE_PATH, 'button.png')
COST = join(FEATURE_PATH, 'cost.png')

COSTS = {
    1: join(FEATURE_PATH, 'cost-1.png'),
    2: join(FEATURE_PATH, 'cost-2.png'),
    3: join(FEATURE_PATH, 'cost-3.png'),
    4: join(FEATURE_PATH, 'cost-4.png'),
    5: join(FEATURE_PATH, 'cost-5.png')
}


@feature('farm pvp')
@farm_exceptions
def go_pvp(is_loop=False, cost=1, **kwargs):
    kwargs['cost'] = COSTS[cost]
    run_pvp(**kwargs)
    while is_loop:
        run_pvp(**kwargs)


@go_main_screen
def run_pvp(**kwargs):
    find_image_and_click_then_sleep(BTN, retry_time=5)

    find_image_and_click_then_sleep(COST, retry_time=5)

    try:
        img_cost = kwargs.get('cost', COSTS[1])
        find_image_and_click_then_sleep(img_cost, retry_time=5, sleep_duration=0.5)
        find_image(img_cost)
        press_escape()
    except:
        pass

    find_image_and_click_then_sleep(COMMON_PLAY, retry_time=5)
    sleep(0.5)
    
    run_or_raise_exception(
        lambda: find_image_and_click_then_sleep(COMMON_NO_BTN),
        NoEnergyException
    )
    
    find_image_and_click_then_sleep(COMMON_FIGHT)
    find_image_and_click_then_sleep(COMMON_ACCEPT)

    try:
        find_image(COMMON_AUTO_ON)
    except:
        try:
            find_image_and_click_then_sleep(COMMON_AUTO_OFF)
        except:
            pass

    while True:
        try:
            y, x = find_image(COMMON_TOWN, retry_time=1)
            sleep(1)
            click_screen_and_sleep(y, x)
            break
        except:
            pass
