from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from utils import click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'gvg')
BTN = join(FEATURE_PATH, 'button.png')


@feature('gvg')
@is_run
@go_main_screen
@farm_exceptions
def go_gvg(is_loop=True, **kwargs):
    cost = COSTS.get(kwargs.get('cfg', {}).get('cost', 1), 1)

    find_image_and_click_then_sleep(BTN, retry_time=5)
    run_gvg(cost)
    while is_loop:
        run_gvg(cost)


def run_gvg(cost):
    click_cost_and_play(cost)
    find_image_and_click_then_sleep(COMMON_FIGHT)
    find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
    find_image_and_click_then_sleep(COMMON_ACCEPT)

    fight_wait_town()
