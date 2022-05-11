from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from utils import check_no_energy, click_cost_and_play, click_town, enable_auto_on, fight_wait_town, find_image, find_image_and_click_then_sleep, run_or_raise_exception, sleep
from window import press_escape


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
    click_cost_and_play(kwargs.get('cost', COSTS[1]))
    
    find_image_and_click_then_sleep(COMMON_FIGHT)
    find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
    find_image_and_click_then_sleep(COMMON_ACCEPT)

    fight_wait_town()
