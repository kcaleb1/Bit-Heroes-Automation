from error import InvalidValueValidateException
from farm import Farm
from const import *
from ui.farm.pvp import PvpConfigUI
from utils import check_no_energy, click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'pvp')
BTN = join(FEATURE_PATH, 'button.png')


class Pvp(Farm):
    feature = 'pvp'
    configUI = PvpConfigUI

    def __init__(self):
        super().__init__()

    def do_run(self):
        find_image_and_click_then_sleep(BTN, retry_time=5)
        click_cost_and_play(COSTS[self.cost])
        find_image_and_click_then_sleep(COMMON_FIGHT, sleep_duration=0.5)
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
