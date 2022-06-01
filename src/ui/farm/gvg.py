from const import LIST_COSTS
from ui.farm import ConfigUI, Farm
from ui.farm.utils import create_option_menu


class GvgConfigUI(ConfigUI):
    def __init__(self, farm: Farm, parent, main) -> None:
        super().__init__(farm, parent, main)

    def _add_config_frames(self):
        self.cost = create_option_menu(self.root,
                                       data=LIST_COSTS,
                                       value=self.farm.cost,
                                       name='cost')

    def _do_save_config(self):
        self.farm.cfg['cost'] = self.cost.get()
