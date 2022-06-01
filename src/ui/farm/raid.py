from const import LIST_DIFFICULTIES
from ui.farm import ConfigUI, Farm
from ui.farm.utils import create_option_menu


class RaidConfigUI(ConfigUI):
    def __init__(self, farm: Farm, parent, main) -> None:
        super().__init__(farm, parent, main)

    def _add_config_frames(self):
        self.boss = create_option_menu(self.root,
                                       data=self.farm.bosses,
                                       value=self.farm.boss,
                                       name='boss')
        self.difficulty = create_option_menu(self.root,
                                             data=LIST_DIFFICULTIES,
                                             value=self.farm.difficulty,
                                             name='difficulty')

    def _do_save_config(self):
        self.farm.cfg['boss'] = self.boss.get()
        self.farm.cfg['difficulty'] = self.difficulty.get()
