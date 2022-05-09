from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from error import NoEnergyException
from utils import check_no_energy, click_town, enable_auto_on, find_image, find_image_and_click_then_sleep, run_or_raise_exception, sleep
from window import click_screen_and_sleep, press_escape


FEATURE_PATH = join(IMG_PATH, 'gauntlet')
BTN = join(FEATURE_PATH, 'button.png')
COST = join(FEATURE_PATH, 'cost.png')


@feature('gauntlet')
@is_run
@go_main_screen
@farm_exceptions
def go_gauntlet(is_loop=True, **kwargs):
    cost = kwargs.get('cfg', {}).get('cost', 1)
    kwargs['cost'] = COSTS.get(cost, 1)

    find_image_and_click_then_sleep(BTN, retry_time=5)

    run_gauntlet(**kwargs)
    while is_loop:
        run_gauntlet(**kwargs)


def run_gauntlet(**kwargs):
    find_image_and_click_then_sleep(COST, retry_time=5)

    try:
        img_cost = kwargs.get('cost')
        find_image_and_click_then_sleep(img_cost, retry_time=5, sleep_duration=0.5)
        find_image(img_cost)
        press_escape()
    except:
        pass

    find_image_and_click_then_sleep(COMMON_PLAY, retry_time=5)
    sleep(0.5)
    
    check_no_energy()
    
    find_image_and_click_then_sleep(COMMON_ACCEPT)
    enable_auto_on()

    while not click_town():
        sleep(1)
