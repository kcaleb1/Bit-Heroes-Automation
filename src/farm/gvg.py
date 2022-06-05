from const import *
from farm import Farm
from error import InvalidValueValidateException
from ui.farm.gvg import GvgConfigUI
from utils import click_play_and_check_no_energy, fight_wait_town, find_image_and_click_then_sleep, select_cost


FEATURE_PATH = join(IMG_PATH, 'gvg')
BTN = join(FEATURE_PATH, 'button.png')


class Gvg(Farm):
    feature = 'gvg'
    configUI = GvgConfigUI

    def __init__(self):
        super().__init__()

    def select_run(self):
        find_image_and_click_then_sleep(BTN, retry_time=5)
        select_cost(COSTS[self.cost])

    def main_run(self):
        click_play_and_check_no_energy(keep_guide=True)
        find_image_and_click_then_sleep(COMMON_FIGHT)
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM, sleep_duration=0.5)
        find_image_and_click_then_sleep(COMMON_ACCEPT)
        fight_wait_town()

    def mapping_config(self):
        super().mapping_config()
        self.cost = self.cfg.get('cost', 1)

    def validate(self):
        super().validate()
        if self.cost not in range(1, 5+1):
            raise InvalidValueValidateException(
                farm=self.feature, key='cost',
                value=self.cost, expect='not in 1-5')

    def __str__(self) -> str:
        return '\n'.join([super().__str__(),
                          f"Cost: {self.cost}"])
