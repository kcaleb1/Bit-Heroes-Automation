from farm import Farm
from time import sleep
from utils import check_no_energy, click_town, decline_except_persure, enable_auto_on, find_image_and_click_then_sleep, find_image, run_or_raise_exception
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


class Raid(Farm):
    def __init__(self):
        super().__init__('raid')

    def do_run(self):
        find_image_and_click_then_sleep(BTN)

        while True:
            try:
                find_image(BOSSES[self.boss], retry_time=1)
                break
            except:
                find_image_and_click_then_sleep(MOVE_LEFT)
                sleep(0.5)

        find_image_and_click_then_sleep(SUMMON_BTN)
        find_image_and_click_then_sleep(DIFFICULTIES[self.difficulty])
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
        find_image_and_click_then_sleep(COMMON_ACCEPT, sleep_duration=1)
        check_no_energy()

        while not enable_auto_on():
            sleep(SLEEP)

        while True:
            if click_town():
                return
            decline_except_persure(DECLINE)

    def mapping_config(self):
        super().mapping_config()
        self.boss = self.cfg.get('boss', 1)
        self.difficulty = self.cfg.get(
            'difficulty', list(DIFFICULTIES.keys())[0])

    def validate(self):
        super().validate()
        if self.boss not in range(1, 4+1):
            raise InvalidValueValidateException(
                key='boss', value=self.boss, expect='in 1-4')
        if self.difficulty not in DIFFICULTIES.keys():
            raise InvalidValueValidateException(
                key='difficulty', value=self.difficulty, expect=f'not in {DIFFICULTIES.keys()}')
