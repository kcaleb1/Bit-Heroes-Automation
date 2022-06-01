from const import *
from error import InvalidValueValidateException
from farm import Farm
from ui.farm.expedition import ExpeditionConfigUI
from utils import click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'expedition')
BTN = join(FEATURE_PATH, 'button.png')
ENTER = join(FEATURE_PATH, 'enter.png')

ZONES = {
    "Burning Farm": join(FEATURE_PATH, 'burning-farm.png'),
    "Hero Fest": join(FEATURE_PATH, 'hero-fest.png'),
    "Melvapaloozo": join(FEATURE_PATH, 'melvapaloozo.png')
}


class Expedition(Farm):
    feature = 'expedition'
    zones = list(ZONES.keys())
    configUI = ExpeditionConfigUI

    def __init__(self):
        super().__init__()

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
        if self.cost not in LIST_COSTS:
            raise InvalidValueValidateException(
                farm=self.feature, key='cost',
                value=self.cost, expect=f'not in {LIST_COSTS}')
        if self.zone not in self.zones:
            raise InvalidValueValidateException(
                key='zone', value=self.zone, expect=f'not in {self.zones}')

    def __str__(self) -> str:
        return '\n'.join([super().__str__(),
                          f"Cost: {self.cost}",
                          f"Zone: {self.zone}"])
