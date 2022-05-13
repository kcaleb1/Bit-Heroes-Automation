from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from utils import click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'pvp')
BTN = join(FEATURE_PATH, 'button.png')


@feature('pvp')
@is_run
@go_main_screen
@farm_exceptions
def go_pvp(is_loop=True, **kwargs):
    cost = kwargs.get('cfg', {}).get('cost', 1)
    kwargs['cost'] = COSTS.get(cost)
    find_image_and_click_then_sleep(BTN, retry_time=5)
    run_pvp(**kwargs)
    while is_loop:
        run_pvp(**kwargs)


def run_pvp(**kwargs):
    click_cost_and_play(kwargs.get('cost', COSTS[1]))
    find_image_and_click_then_sleep(COMMON_FIGHT)
    find_image_and_click_then_sleep(COMMON_ACCEPT)
    fight_wait_town()
