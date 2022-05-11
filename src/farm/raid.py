from time import sleep
from decorator import feature, go_main_screen, farm_exceptions, is_run
from utils import check_no_energy, click_town, enable_auto_on, find_image_and_click_then_sleep, find_image, run_or_raise_exception
from const import *
from error import *


FEATURE_PATH = join(IMG_PATH, 'raid')
BTN = join(FEATURE_PATH, 'button.png')
MOVE_LEFT = join(FEATURE_PATH, 'move-left.png')
SUMMON_BTN = join(FEATURE_PATH, 'summon.png')
DECLINE = join(FEATURE_PATH, 'decline.png')

BOSSES = {
    1: join(FEATURE_PATH, 'boss-1.png'),
    2: join(FEATURE_PATH, 'boss-2.png'),
    3: join(FEATURE_PATH, 'boss-3.png'),
    4: join(FEATURE_PATH, 'boss-4.png')
}


@feature('raid')
@is_run
@farm_exceptions
def go_raid(is_loop=True, **kwargs):
    boss = kwargs.get('cfg', {}).get('boss', 1)
    difficulty= kwargs.get('cfg', {}).get('difficulty', 1)

    do_raid(boss, difficulty)
    while is_loop:
        do_raid(boss, difficulty)

@go_main_screen
def do_raid(boss, difficulty):
    find_image_and_click_then_sleep(BTN)

    while True:
        try:
            find_image(BOSSES[boss], retry_time=1)
            break
        except:
            find_image_and_click_then_sleep(MOVE_LEFT)
            sleep(0.5)

    find_image_and_click_then_sleep(SUMMON_BTN)
    find_image_and_click_then_sleep(DIFFICULTIES[difficulty])

    find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
    find_image_and_click_then_sleep(COMMON_ACCEPT)
    
    check_no_energy()

    while not enable_auto_on(): sleep(SLEEP)

    while True:
        if click_town():
            return
        
        try:
            find_image_and_click_then_sleep(DECLINE, retry_time=1)
            find_image_and_click_then_sleep(COMMON_YES, retry_time=1)
        except:
            pass
