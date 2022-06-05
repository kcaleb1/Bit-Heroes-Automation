from const import *
from error import InvalidValueValidateException
from farm import Farm
from ui.farm.expedition import ExpeditionConfigUI
from utils import check_no_energy, click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep, select_cost


FEATURE_PATH = join(IMG_PATH, 'expedition')
BTN = join(FEATURE_PATH, 'button.png')
ENTER = join(FEATURE_PATH, 'enter.png')

ZONES = {
    1: join(FEATURE_PATH, 'burning-farm.png'),
    2: join(FEATURE_PATH, 'hero-fest.png'),
    3: join(FEATURE_PATH, 'melvapaloozo.png')
}


class Expedition(Farm):
    feature = 'expedition'
    zones = list(ZONES.keys())
    configUI = ExpeditionConfigUI

    def __init__(self):
        super().__init__()

    # TODO find way to dynamic zone image
    def select_run(self):
        find_image_and_click_then_sleep(BTN, retry_time=5)
        click_cost_and_play(COSTS[self.cost], keep_guide=True)
        find_image_and_click_then_sleep(ZONES.get(self.zone))

    def main_run(self):
        find_image_and_click_then_sleep(ENTER)
        check_no_energy(keep_guide=True)
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
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
