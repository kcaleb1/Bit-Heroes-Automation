from time import sleep
from setuptools import find_namespace_packages
from decorator import farm_exceptions, feature, go_main_screen, is_run
from const import *
from error import MismatchConditionException
from utils import check_no_energy, click_town, enable_auto_on, fight_wait_town, find_image, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'quest')
BTN = join(FEATURE_PATH, 'button.png')
LEFT = join(FEATURE_PATH, 'left.png')
RIGHT = join(FEATURE_PATH, 'right.png')
DUNGEON = join(FEATURE_PATH, 'dungeon.png')
DECLINE = join(FEATURE_PATH, 'decline.png')
Z1 = join(FEATURE_PATH, 'z1.png')

QUESTS_DIF = {
    1: join(FEATURE_PATH, 'normal.png'),
    2: join(FEATURE_PATH, 'hard.png'),
    3: join(FEATURE_PATH, 'heroic.png')
}

@feature('quest')
@is_run
@go_main_screen
@farm_exceptions
def go_quest(is_loop=True, **kwargs):
    zone = kwargs.get('cfg', {}).get('zone', 1)
    floor = kwargs.get('cfg', {}).get('floor', 1)
    difficulty = kwargs.get('cfg', {}).get('difficulty', 1)
    
    img_quest = join(FEATURE_PATH, f'z{zone}f{floor}.png')
    zone_name = join(FEATURE_PATH, f'z{zone}.png')
    if zone == '13':
        img_quest = DUNGEON

    find_image_and_click_then_sleep(BTN, retry_time=5)
    run_quest(zone, difficulty, img_quest, zone_name)
    while is_loop:
        run_quest(zone, difficulty, img_quest, zone_name)


def run_quest(zone, difficulty, img_quest ,zone_name):
    while True:
        try:
            find_image(zone_name, retry_time=1)
            break
        except:
            pass
        find_image_and_click_then_sleep(LEFT, retry_time=1, ignore_exception=True)
        try:
            find_image(Z1, retry_time=1)
            cur_zone = 1
            while cur_zone != zone:
                find_image_and_click_then_sleep(RIGHT, ignore_exception=True)
                cur_zone += 1
            break
        except:
            pass
    
    find_image_and_click_then_sleep(img_quest, sleep_duration=1)
    find_image_and_click_then_sleep(QUESTS_DIF[difficulty])
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
