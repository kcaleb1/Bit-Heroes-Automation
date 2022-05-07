from decorator import farm_exceptions, feature, go_main_screen
from const import *
from utils import find_image, find_image_and_click_then_sleep, sleep
from window import click_screen_and_sleep, press_escape

FEATURE_PATH = join(IMG_PATH, 'raid')
BTN = join(FEATURE_PATH, 'button.png')
COST = join(FEATURE_PATH, 'cost.png')
COST_1 = join(FEATURE_PATH, 'cost-1.png')
COST_2 = join(FEATURE_PATH, 'cost-2.png')
COST_3 = join(FEATURE_PATH, 'cost-3.png')
COST_4 = join(FEATURE_PATH, 'cost-4.png')
COST_5 = join(FEATURE_PATH, 'cost-5.png')

COSTS = {
    1: COST_1,
    2: COST_2,
    3: COST_3,
    4: COST_4,
    5: COST_5
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
        find_image_and_click_then_sleep(
            kwargs.get('cost', COST_1), retry_time=5)
    except:
        press_escape()

    find_image_and_click_then_sleep(COMMON_PLAY, retry_time=5)

    try:
        find_image(COMMON_AUTO_ON, retry_time=3)
    except:
        try:
            find_image_and_click_then_sleep(COMMON_AUTO_OFF, retry_time=3)
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
