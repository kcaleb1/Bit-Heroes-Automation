from const import *
from error import InvalidValueValidateException
from farm import Farm
from ui.farm.invasion import InvasionConfigUI
from utils import click_play_and_check_no_energy, fight_wait_town, find_image_and_click_then_sleep, select_cost


FEATURE_PATH = join(IMG_PATH, 'invasion')
BTN = join(FEATURE_PATH, 'button.png')


class Invasion(Farm):
    feature = 'invasion'
    configUI = InvasionConfigUI

    def __init__(self):
        super().__init__()
        self.button = BTN

    def config_run(self):
        select_cost(COSTS[self.cost], COMMON_COST)

    def main_run(self):
        click_play_and_check_no_energy()
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM, sleep_duration=0.5)
        find_image_and_click_then_sleep(COMMON_ACCEPT, sleep_duration=1)
        fight_wait_town()

    def mapping_config(self):
        super().mapping_config()
        self.cost = self.cfg.get('cost', 1)

    def validate(self):
        super().validate()
        if self.cost not in LIST_COSTS:
            raise InvalidValueValidateException(
                farm=self.feature, key='cost',
                value=self.cost, expect=f'not in {LIST_COSTS}')

    def __str__(self) -> str:
        return '\n'.join([super().__str__(),
                          f"Cost: {self.cost}"])
