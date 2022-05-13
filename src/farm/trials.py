from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from utils import click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'trials')
BTN = join(FEATURE_PATH, 'button.png')
PLAY = join(FEATURE_PATH, 'play.png')


@feature('trials')
@is_run
@go_main_screen
@farm_exceptions
def go_trials(is_loop=True, **kwargs):
    cost = kwargs.get('cfg', {}).get('cost', 1)
    kwargs['cost'] = COSTS.get(cost, 1)

    find_image_and_click_then_sleep(BTN, retry_time=5)
    run_trials(**kwargs)
    while is_loop:
        run_trials(**kwargs)


def run_trials(**kwargs):
    click_cost_and_play(kwargs.get('cost'), COMMON_SPECIAL_COST, play_btn=PLAY)
    find_image_and_click_then_sleep(COMMON_ACCEPT, sleep_duration=1)
    fight_wait_town()
