from utils import find_image_and_click_then_sleep, find_image, go_main_screen
from window import click_screen_and_sleep
from const import *
from error import *

bosses = {
    1: RAID_BOSS_1,
    2: RAID_BOSS_2,
    3: RAID_BOSS_3
}

difficulties = {
    1: COMMON_NORMAL,
    2: COMMON_HARD,
    3: COMMON_HEROIC
}

def go_raid(is_loop=False, boss=3, difficulty=3):
    go_main_screen()

    try:
        find_image_and_click_then_sleep(RAID_BTN)

        try:
            find_image(RAID_NO_RAID)
            raise NoRaidEnergyException()
        except NoRaidEnergyException as e:
            raise e
        except:
            pass

        while True:
            try:
                find_image(bosses[boss], retry_time=1)
                break
            except:
                find_image_and_click_then_sleep(RAID_MOVE_LEFT_BTN)

        find_image_and_click_then_sleep(RAID_SUMMON_BTN)
        find_image_and_click_then_sleep(difficulties[difficulty])

        do_raid()
        while is_loop:
            do_raid()

    except NoRaidEnergyException as e:
        print(e.__str__())
    except Exception as e:
        print('got error when go_raid: ', e)

def do_raid():

    find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
    find_image_and_click_then_sleep(COMMON_ACCEPT)

    while True:
        try:
            find_image(COMMON_AUTO_ON)
            break
        except:
            try: find_image_and_click_then_sleep(COMMON_AUTO_OFF)
            except: pass
            break

    try: find_image_and_click_then_sleep(COMMON_RERUN, retry_time=100, sleep_duration=2)
    except: find_image_and_click_then_sleep(COMMON_TOWN, retry_time=100, sleep_duration=2)
    