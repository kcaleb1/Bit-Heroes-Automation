from const import *
from error import InvalidValueValidateException
from farm import Farm
from ui.farm.trials import TrailsConfigUI
from utils import click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'trials')
BTN = join(FEATURE_PATH, 'button.png')
PLAY = join(FEATURE_PATH, 'play.png')


class Trails(Farm):
    feature = 'trails'
    configUI = TrailsConfigUI

    def __init__(self):
        super().__init__()

    def select_run(self):
        find_image_and_click_then_sleep(BTN, retry_time=5)
        click_cost_and_play(
            COSTS[self.cost], COMMON_SPECIAL_COST, play_btn=PLAY)

    def main_run(self):
        find_image_and_click_then_sleep(COMMON_ACCEPT, sleep_duration=1)
        fight_wait_town()

    def mapping_config(self):
        super().mapping_config()
        self.cost = self.cfg.get('cost', 1)

    def validate(self):
        super().validate()
        if not self.cost in range(1, 5+1):
            raise InvalidValueValidateException(
                farm=self.feature, key='cost',
                value=self.cost, expect='not in 1-5')

    def __str__(self) -> str:
        return '\n'.join([super().__str__(),
                          f"Cost: {self.cost}\n"])
