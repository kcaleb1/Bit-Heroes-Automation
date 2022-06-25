from error import InvalidValueValidateException
from farm import Farm
from const import *
from ui.farm.pvp import PvpConfigUI
from utils import click_play_and_check_no_energy, fight_wait_town, find_image_and_click_then_sleep, select_cost


FEATURE_PATH = join(IMG_PATH, 'pvp')
BTN = join(FEATURE_PATH, 'button.png')
NO_ENERGY_BAR = join(FEATURE_PATH, 'no-energy-bar.png')


class Pvp(Farm):
    feature = 'pvp'
    configUI = PvpConfigUI
    default_config = {
        'cost': LIST_COSTS[0]
    }

    def __init__(self):
        super().__init__()
        self.button = BTN
        # self.no_energy_bars = [NO_ENERGY_BAR]
        self.no_energy_bars = []

    def config_run(self):
        super().config_run()
        select_cost(COSTS[self.cost])

    def main_run(self):
        click_play_and_check_no_energy()
        find_image_and_click_then_sleep(COMMON_FIGHT, sleep_duration=0.5)
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
