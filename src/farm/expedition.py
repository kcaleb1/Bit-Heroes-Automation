from debug import save_image_dbg
from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from utils import click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep
from window import get_game_screen


FEATURE_PATH = join(IMG_PATH, 'expedition')
BTN = join(FEATURE_PATH, 'button.png')
Z1 = join(FEATURE_PATH, 'burning-farm.png')
Z2 = join(FEATURE_PATH, 'hero-fest.png')
Z3 = join(FEATURE_PATH, 'melvapaloozo.png')
ENTER = join(FEATURE_PATH, 'enter.png')

ZONES = [Z1, Z2, Z3]


@feature('expedition')
@is_run
@go_main_screen
@farm_exceptions
def go_expedition(is_loop=True, **kwargs):
    cost = COSTS.get(kwargs.get('cfg', {}).get('cost', 1), 1)

    find_image_and_click_then_sleep(BTN, retry_time=5)
    run_expedition(cost)
    while is_loop:
        run_expedition(cost)


def run_expedition(cost):
    click_cost_and_play(cost)
    is_zone = False
    for z in ZONES:
        try:
            find_image_and_click_then_sleep(z)
            is_zone = True
            break
        except:
            pass

    if not is_zone:
        save_image_dbg('?????', get_game_screen())
        raise Exception('?????????')

    find_image_and_click_then_sleep(ENTER)
    find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
    find_image_and_click_then_sleep(COMMON_ACCEPT)
    fight_wait_town()
