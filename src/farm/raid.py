from time import sleep
from utils import find_image_and_click_then_sleep, find_image, go_main_screen, run_or_raise_exception
from window import click_screen_and_sleep
from const import *
from error import *


IMAGE_PATH = join(CUR_PATH, 'img', 'raid')
BTN = join(IMAGE_PATH, 'button.png')
MOVE_RIGHT_BTN = join(IMAGE_PATH, 'move-right.png')
MOVE_LEFT_BTN = join(IMAGE_PATH, 'move-left.png')
SUMMON_BTN = join(IMAGE_PATH, 'summon.png')
BOSS_1 = join(IMAGE_PATH, 'boss-1.png')
BOSS_2 = join(IMAGE_PATH, 'boss-2.png')
BOSS_3 = join(IMAGE_PATH, 'boss-3.png')
NO_RAID = join(IMAGE_PATH, 'no-raid.png')

BOSSES = {
    1: BOSS_1,
    2: BOSS_2,
    3: BOSS_3
}


def go_raid(is_loop=False, boss=3, difficulty=3):
    go_main_screen()

    try:
        find_image_and_click_then_sleep(BTN)

        run_or_raise_exception(
            lambda: find_image(NO_RAID, threshold=0.9),
            NoRaidEnergyException
        )

        while True:
            try:
                find_image(BOSSES[boss], retry_time=1)
                break
            except:
                find_image_and_click_then_sleep(MOVE_LEFT_BTN)

        find_image_and_click_then_sleep(SUMMON_BTN)
        find_image_and_click_then_sleep(DIFFICULTIES[difficulty])

        find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
        find_image_and_click_then_sleep(COMMON_ACCEPT)

        do_raid()
        while is_loop:
            do_raid()

    except NoRaidEnergyException as ex:
        print(ex.__str__())
    except KeyboardInterrupt as ex:
        raise ex
    except Exception as ex:
        print('got error when go_raid: ', ex)


def do_raid():
    run_or_raise_exception(
        lambda: find_image_and_click_then_sleep(
            COMMON_NO_BTN, threshold=0.9, retry_time=20),
        NoRaidEnergyException
    )

    while True:
        try:
            find_image(COMMON_AUTO_ON)
            break
        except:
            try:
                find_image_and_click_then_sleep(COMMON_AUTO_OFF)
            except:
                pass
            break

    while True:
        try:
            y, x = find_image(COMMON_RERUN)
            sleep(1)
            click_screen_and_sleep(y, x)
            break
        except:
            pass
