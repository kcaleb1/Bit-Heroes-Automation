from const import *
from error import InvalidValueValidateException
from farm import Farm
from utils import click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'expedition')
BTN = join(FEATURE_PATH, 'button.png')
Z1 = join(FEATURE_PATH, 'burning-farm.png')
Z2 = join(FEATURE_PATH, 'hero-fest.png')
Z3 = join(FEATURE_PATH, 'melvapaloozo.png')
ENTER = join(FEATURE_PATH, 'enter.png')

ZONES = {
    1: Z1,
    2: Z2,
    3: Z3
}


class Expedition(Farm):
    def __init__(self):
        super().__init__('expedition')

    def do_run(self):
        find_image_and_click_then_sleep(BTN, retry_time=5)
        click_cost_and_play(COSTS[self.cost])
        find_image_and_click_then_sleep(ZONES.get(self.zone))
        find_image_and_click_then_sleep(ENTER)
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM, sleep_duration=0.5)
        find_image_and_click_then_sleep(COMMON_ACCEPT)
        fight_wait_town()

    def mapping_config(self):
        super().mapping_config()
        self.cost = self.cfg.get('cost', 1)
        self.zone = self.cfg.get('zone', 1)

    def validate(self):
        super().validate()
        if self.cost not in range(1, 3+1):
            raise InvalidValueValidateException(
                farm=self.feature, key='cost',
                value=self.cost, expect='not in 1-3')
        if self.zone not in range(1, 3+1):
            raise InvalidValueValidateException(
                key='zone', value=self.zone, expect='not in 1-3')

    def __str__(self) -> str:
        return super().__str__() + f"Cost: {self.cost}\nZone: {self.zone}"
