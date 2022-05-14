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
    cost = COSTS.get(kwargs.get('cfg', {}).get('cost', 1), 1)
    find_image_and_click_then_sleep(BTN, retry_time=5)
    run_pvp(cost)
    while is_loop:
        run_pvp(cost)


def run_pvp(cost):
    click_cost_and_play(cost)
    find_image_and_click_then_sleep(COMMON_FIGHT)
    find_image_and_click_then_sleep(COMMON_ACCEPT)
    fight_wait_town()
