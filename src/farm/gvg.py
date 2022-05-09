from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from error import NoEnergyException
from utils import check_no_energy, click_town, enable_auto_on, find_image, find_image_and_click_then_sleep, run_or_raise_exception, sleep
from window import click_screen_and_sleep, press_escape


FEATURE_PATH = join(IMG_PATH, 'gvg')
BTN = join(FEATURE_PATH, 'button.png')


@feature('gvg')
@is_run
@go_main_screen
@farm_exceptions
def go_gvg(is_loop=True, **kwargs):
    cost = kwargs.get('cfg', {}).get('cost', 1)
    kwargs['cost'] = COSTS.get(cost, 1)

    find_image_and_click_then_sleep(BTN, retry_time=5)

    run_gvg(**kwargs)
    while is_loop:
        run_gvg(**kwargs)


def run_gvg(**kwargs):
    find_image_and_click_then_sleep(COMMON_COST, retry_time=5)

    try:
        img_cost = kwargs.get('cost', COSTS[1])
        find_image_and_click_then_sleep(img_cost, retry_time=5, sleep_duration=0.5)
        find_image(img_cost)
        press_escape()
    except:
        pass

    find_image_and_click_then_sleep(COMMON_PLAY, retry_time=5)
    sleep(0.5)
    
    check_no_energy()
    
    find_image_and_click_then_sleep(COMMON_FIGHT)
    find_image_and_click_then_sleep(COMMON_ACCEPT)

    enable_auto_on()

    while not click_town():
        sleep(1)
