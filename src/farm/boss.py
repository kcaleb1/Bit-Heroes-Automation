from farm import Farm
from utils import check_no_energy, click_town, enable_auto_on, find_image, find_image_and_click_then_sleep, raise_exception_when_runnable, sleep
from window import press_escape
from const import *
from error import *
from datetime import datetime


FEATURE_PATH = join(IMG_PATH, 'boss')
BTN = join(FEATURE_PATH, 'button.png')
FULL_TXT = join(FEATURE_PATH, 'full.png')
JOIN_BTN = join(FEATURE_PATH, 'join.png')
READY_BTN = join(FEATURE_PATH, 'ready.png')
START_BTN = join(FEATURE_PATH, 'start.png')


class Boss(Farm):
    feature = 'boss'

    def __init__(self):
        super().__init__()

    def do_run(self):
        find_image_and_click_then_sleep(BTN)
        try:
            find_image_and_click_then_sleep(
                JOIN_BTN, retry_time=5, sleep_duration=1)
        except:
            raise UnableJoinBossException()

        check_no_energy()
        for _ in range(10):
            try:
                find_image_and_click_then_sleep(READY_BTN, retry_time=1)
                break
            except:
                pass
            raise_exception_when_runnable(
                lambda: find_image(COMMON_CLOSE, retry_time=1),
                UnableJoinBossException
            )
        else:
            raise UnableJoinBossException()

        start_time = datetime.now()
        is_started = False
        is_auto_on = False
        is_pressed_escape = False
        while True:
            is_started = click_town()
            if is_started:
                break

            if not is_auto_on:
                # check got kicked from room
                raise_exception_when_runnable(
                    lambda: find_image_and_click_then_sleep(
                        COMMON_CLOSE, retry_time=1),
                    UnableJoinBossException
                )

                # check when become host, leave lobby and rerun
                try:
                    find_image(START_BTN, retry_time=1)
                    press_escape()
                    break
                except:
                    pass

                # this will help to exit the lobby when host afk to long
                # press escape, in case of already in-game, this will turn off auto play
                # and the click COMMON_AUTO_OFF will handle it
                if (datetime.now() - start_time).seconds >= 60:
                    if is_pressed_escape:
                        break
                    press_escape()
                    is_pressed_escape = True

                is_auto_on = enable_auto_on()

        if not is_started:
            sleep(0.5)
            find_image_and_click_then_sleep(COMMON_YES)
            raise UnableJoinBossException()
