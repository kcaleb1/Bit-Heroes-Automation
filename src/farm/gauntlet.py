from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from utils import check_no_energy, click_cost_and_play, click_town, enable_auto_on, fight_wait_town, find_image, find_image_and_click_then_sleep, run_or_raise_exception, sleep
from window import press_escape


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
    click_cost_and_play(kwargs.get('cost'), COST)
    
    find_image_and_click_then_sleep(COMMON_ACCEPT, sleep_duration=1)
    fight_wait_town()
