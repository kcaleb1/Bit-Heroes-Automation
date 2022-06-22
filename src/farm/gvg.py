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
    default_config = {
        'cost': LIST_COSTS[0]
    }

    def __init__(self):
        super().__init__()
        self.button = BTN

    def config_run(self):
        select_cost(COSTS[self.cost])

    def main_run(self):
        click_play_and_check_no_energy(keep_guide=True)
        find_image_and_click_then_sleep(COMMON_FIGHT)
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM, sleep_duration=0.5)
        find_image_and_click_then_sleep(COMMON_ACCEPT)
        fight_wait_town()

    def mapping_config(self):
        super().mapping_config()
        self.cost = self.cfg.get('cost', self.default_config['cost'])

    def validate(self):
        super().validate()
        if self.cost not in LIST_COSTS:
            raise InvalidValueValidateException(
                farm=self.feature, key='cost',
                value=self.cost, expect=f'not in {LIST_COSTS}')

    def __str__(self) -> str:
        return '\n'.join([super().__str__(),
                          f"Cost: {self.get_cost_from_usage()}"])
