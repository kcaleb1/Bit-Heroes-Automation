from farm import Farm
from time import sleep
from const import *
from error import InvalidValueValidateException
from utils import check_no_energy, click_town, decline_except_persure, enable_auto_on, find_image, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'quest')
BTN = join(FEATURE_PATH, 'button.png')
LEFT = join(FEATURE_PATH, 'left.png')
RIGHT = join(FEATURE_PATH, 'right.png')
DUNGEON = join(FEATURE_PATH, 'dungeon.png')
DECLINE = join(FEATURE_PATH, 'decline.png')
DECLINE_MERCHANTS = join(FEATURE_PATH, 'decline-merchants.png')
Z1 = join(FEATURE_PATH, 'z1.png')

DUNGEON_NUM = 99

QUESTS_DIF = {
    'normal': join(FEATURE_PATH, 'normal.png'),
    'hard': join(FEATURE_PATH, 'hard.png'),
    'heroic': join(FEATURE_PATH, 'heroic.png')
}


class Quest(Farm):
    def __init__(self):
        super().__init__('quest')

    def do_run(self):
        find_image_and_click_then_sleep(BTN, retry_time=5)
        cur_img = None
        while True:
            try:
                find_image(self.zone_name, retry_time=1, threshold=0.9)
                break
            except:
                pass
            find_image_and_click_then_sleep(
                LEFT, retry_time=1, ignore_exception=True)
            try:
                find_image(Z1, retry_time=1,
                           game_screen=cur_img, threshold=0.9)
                cur_zone = 1
                while cur_zone != self.zone:
                    find_image_and_click_then_sleep(
                        RIGHT, ignore_exception=True)
                    cur_zone += 1
                break
            except:
                pass

        find_image_and_click_then_sleep(self.img_quest, sleep_duration=1)
        find_image_and_click_then_sleep(QUESTS_DIF[self.difficulty])
        find_image_and_click_then_sleep(COMMON_ACCEPT)
        check_no_energy()

        while not enable_auto_on():
            sleep(SLEEP)

        while True:
            if click_town():
                return
            decline_except_persure(DECLINE)
            decline_except_persure(DECLINE_MERCHANTS)

    def mapping_config(self):
        super().mapping_config()
        self.zone = self.cfg.get('zone', 1)
        self.floor = self.cfg.get('floor', 1)
        self.difficulty = self.cfg.get(
            'difficulty', list(DIFFICULTIES.keys())[0])

        self.zone_name = join(FEATURE_PATH, f'z{self.zone}.png')
        if self.floor == DUNGEON_NUM:
            self.img_quest = DUNGEON
        else:
            self.img_quest = join(
                FEATURE_PATH, f'z{self.zone}f{self.floor}.png')

    def validate(self):
        super().validate()
        if not self.zone > 0:
            raise InvalidValueValidateException(
                key='zone', value=self.zone, expect='> 0')
        if self.floor not in range(1, 12+1) and self.floor != 99:
            raise InvalidValueValidateException(
                key='zone', value=self.zone, expect='>= 0 and < 12 or equal 99 (for dungeon)')
        if self.difficulty not in DIFFICULTIES.keys():
            raise InvalidValueValidateException(
                key='difficulty', value=self.difficulty, expect=f'not in {DIFFICULTIES.keys()}')
