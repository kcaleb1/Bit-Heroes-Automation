from farm import Farm
from time import sleep
from const import *
from error import InvalidValueValidateException
from ui.farm.quest import QuestConfigUI
from utils import check_no_energy, click_town_or_rerun, decline_except_persuade, enable_auto_on, find_image, find_image_and_click_then_sleep, open_treasure


FEATURE_PATH = join(IMG_PATH, 'quest')
ZONE_PATH = join(FEATURE_PATH, 'zone')

BTN = join(FEATURE_PATH, 'button.png')
LEFT = join(FEATURE_PATH, 'left.png')
RIGHT = join(FEATURE_PATH, 'right.png')
DECLINE = join(FEATURE_PATH, 'decline.png')
ENTER = join(FEATURE_PATH, 'enter.png')
Z1 = join(ZONE_PATH, 'z1.png')

DELIMITER = "|"

QUESTS_DIF = {
    'Normal': join(FEATURE_PATH, 'normal.png'),
    'Hard': join(FEATURE_PATH, 'hard.png'),
    'Heroic': join(FEATURE_PATH, 'heroic.png')
}

DUNGEON = join(ZONE_PATH, 'dungeon.png')
DUNGEON_NAME = "4|Dungeon"

ZONES = {
    "1|Bit Valley": ["1|Grimz", "2|Dryad", "3|Lord Cerulean", DUNGEON_NAME],
    "2|Wintermarsh": ["1|Yeti", "2|Blubber", "3|Gemm", DUNGEON_NAME],
    "3|Lakehaven": ["1|Nosdoodoo", "2|Jeb", "3|Quirrel", DUNGEON_NAME],
    "4|Ashvale": ["1|Rexie", "2|Warty", "3|Kov'Alg", DUNGEON_NAME],
    "5|Aramore": ["1|Torlim", "2|Zorul", "3|Tealk", DUNGEON_NAME],
    "6|Morgoroth": ["1|Rugumz", "2|Oozmire", "3|Moghur", DUNGEON_NAME],
    "7|Cambora": ["1|Scorpius"],
}

LIST_ZONES = list(ZONES.keys())


class Quest(Farm):
    feature = 'quest'
    zones = ZONES
    list_zone = LIST_ZONES
    configUI = QuestConfigUI

    def __init__(self):
        super().__init__()

    def select_run(self):
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
                while self.list_zone[cur_zone] != self.zone:
                    find_image_and_click_then_sleep(
                        RIGHT, ignore_exception=True)
                    cur_zone += 1
                break
            except:
                pass

        find_image_and_click_then_sleep(self.img_quest, sleep_duration=1)
        if self.dungeon == DUNGEON_NAME:
            find_image_and_click_then_sleep(ENTER)
        else:
            find_image_and_click_then_sleep(QUESTS_DIF[self.difficulty])
        sleep(SLEEP)
        find_image_and_click_then_sleep(COMMON_ACCEPT)

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
            decline_except_persuade(DECLINE)

    def mapping_config(self):
        super().mapping_config()
        self.zone = self.cfg.get('zone', list(self.zones.keys())[0])
        self.dungeon = self.cfg.get('dungeon', ZONES[self.zone][0])
        self.difficulty = self.cfg.get('difficulty', LIST_DIFFICULTIES[0])

        z = self.to_image_name(self.zone)
        d = self.to_image_name(self.dungeon)

        self.zone_name = join(ZONE_PATH, f'z{z}.png')
        if self.dungeon == DUNGEON_NAME:
            self.img_quest = DUNGEON
        else:
            self.img_quest = join(ZONE_PATH, f'z{z}d{d}.png')

    def to_image_name(self, text: str):
        return text.split(DELIMITER)[0]

    def validate(self):
        super().validate()
        if self.zone not in ZONES:
            z = self.zones
            z.sort()
            raise InvalidValueValidateException(
                farm=self.feature, key='zone',
                value=self.zone, expect=f'not in [{z[0]}, {z[len(z)-1]}]')
        if self.dungeon not in ZONES[self.zone]:
            raise InvalidValueValidateException(
                farm=self.feature, key='dungeon',
                value=self.dungeon, expect=f'not in {ZONES[self.zone]}')
        if self.difficulty not in LIST_DIFFICULTIES:
            raise InvalidValueValidateException(
                farm=self.feature, key='difficulty',
                value=self.difficulty, expect=f'not in {LIST_DIFFICULTIES}')

    def __str__(self) -> str:
        z = self.to_image_name(self.zone)
        f = self.to_image_name(self.dungeon)
        return '\n'.join([super().__str__(),
                          f"Zone: Z{z}D{f}",
                          f"Difficulty: {self.difficulty}"])
