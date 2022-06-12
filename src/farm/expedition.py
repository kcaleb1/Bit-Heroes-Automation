from const import *
from error import InvalidValueValidateException, UnableJoinException
from farm import Farm
from ui.farm.expedition import ExpeditionConfigUI
from utils import check_no_energy, click_cost_and_play, fight_wait_town, find_image_and_click_then_sleep


FEATURE_PATH = join(IMG_PATH, 'expedition')
BTN = join(FEATURE_PATH, 'button.png')
ENTER = join(FEATURE_PATH, 'enter.png')

ZONE_PRIORITY = [
    join(FEATURE_PATH, 'zone-low.png'),
    join(FEATURE_PATH, 'zone-medium.png'),
    join(FEATURE_PATH, 'zone-max.png')
]


class Expedition(Farm):
    feature = 'expedition'
    configUI = ExpeditionConfigUI

    def __init__(self):
        super().__init__()

    def select_run(self):
        find_image_and_click_then_sleep(BTN, retry_time=5)
        click_cost_and_play(COSTS[self.cost], keep_guide=True)
        for zone in ZONE_PRIORITY:
            try:
                find_image_and_click_then_sleep(zone, retry_time=4)
                break
            except:
                pass
        else:
            raise UnableJoinException()

    def main_run(self):
        find_image_and_click_then_sleep(ENTER)
        check_no_energy(keep_guide=True)
        find_image_and_click_then_sleep(COMMON_AUTO_TEAM)
        find_image_and_click_then_sleep(COMMON_ACCEPT)
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
