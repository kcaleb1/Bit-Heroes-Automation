from const import DIFFICULTIES
from ui.farm import ConfigUI, Farm
from ui.farm.utils import create_option_menu


class RaidConfigUI(ConfigUI):
    def __init__(self, farm: Farm, parent, main) -> None:
        super().__init__(farm, parent, main)

    def _add_config_frames(self):
        self.boss = create_option_menu(self.root,
                                       data=list(self.farm.bosses.keys()),
                                       value=self.farm.boss,
                                       name='boss')
        self.difficulty = create_option_menu(self.root,
                                             data=list(DIFFICULTIES.keys()),
                                             value=self.farm.difficulty,
                                             name='difficulty')

    def _do_save_config(self):
        self.farm.cfg['boss'] = self.boss.get()
        self.farm.cfg['difficulty'] = self.difficulty.get()
