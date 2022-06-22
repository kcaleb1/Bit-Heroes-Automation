from farm import Farm
from time import sleep
from ui.farm.raid import RaidConfigUI
from utils import check_no_energy, click_town_or_rerun, decline_except_persuade, enable_auto_on, find_image_and_click_then_sleep, find_image, open_treasure
from const import *
from error import *


FEATURE_PATH = join(IMG_PATH, 'raid')
BTN = join(FEATURE_PATH, 'button.png')
MOVE_LEFT = join(FEATURE_PATH, 'move-left.png')
SUMMON_BTN = join(FEATURE_PATH, 'summon.png')
DECLINE = join(FEATURE_PATH, 'decline.png')

BOSSES = {
    "3|Astaroth's Awakening": join(FEATURE_PATH, 'boss-1.png'),
    "4|Hyper Dimension": join(FEATURE_PATH, 'boss-2.png'),
    "5|Woodbeard's Booty": join(FEATURE_PATH, 'boss-3.png'),
    "6|A Haile'Of A Mistake": join(FEATURE_PATH, 'boss-4.png'),
    "7|Zol's Labyrinth": join(FEATURE_PATH, 'boss-5.png'),
    "8|Mallowdale": join(FEATURE_PATH, 'boss-6.png'),
    "9|Gorbon's Rockin' Ruckus": join(FEATURE_PATH, 'boss-7.png'),
    "10|Charred Expanse": join(FEATURE_PATH, 'boss-8.png')
}


class Raid(Farm):
    feature = 'raid'
    bosses = list(BOSSES.keys())
    configUI = RaidConfigUI
    default_config = {
        'boss': list(BOSSES.keys())[0],
        'difficulty': LIST_DIFFICULTIES[0]
    }

    def __init__(self):
        super().__init__()
        self.button = BTN

    def config_run(self):
        for _ in range(len(self.bosses) + 1):
            try:
                find_image(BOSSES[self.boss], retry_time=1)
                break
            except:
                find_image_and_click_then_sleep(MOVE_LEFT)
                sleep(0.5)
        else:
            error = f'Raid {self.boss} not found or tier not reachable'
            self.save_error(error)
            raise CannotRerunException(error)

        find_image_and_click_then_sleep(SUMMON_BTN)
        find_image_and_click_then_sleep(DIFFICULTIES[self.difficulty])
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM, sleep_duration=0.5)
        find_image_and_click_then_sleep(COMMON_ACCEPT, sleep_duration=1)

    def main_run(self):
        check_no_energy()

        while not enable_auto_on():
            sleep(SLEEP)

        while True:
            if click_town_or_rerun(self.rerun_mode):
                return
            if self.decline_treasure:
                decline_except_persuade(COMMON_DECLINE_TREASURE)
            else:
                open_treasure()

    def mapping_config(self):
        super().mapping_config()
        self.boss = self.cfg.get('boss', self.default_config['boss'])
        self.difficulty = self.cfg.get(
            'difficulty', self.default_config['difficulty'])

    def validate(self):
        super().validate()
        if self.boss not in self.bosses:
            raise InvalidValueValidateException(
                farm=self.feature, key='boss',
                value=self.boss, expect=f'not in {self.bosses}')
        if self.difficulty not in DIFFICULTIES.keys():
            raise InvalidValueValidateException(
                farm=self.feature, key='difficulty',
                value=self.difficulty, expect=f'not in {LIST_DIFFICULTIES}')

    def __str__(self) -> str:
        return '\n'.join([super().__str__(),
                          f"Boss: {self.boss}",
                          f"Difficulty: {self.difficulty}"])
