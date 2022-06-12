from const import CONFIG_FILE
from farm import Farm
from ui import BaseConfigUi
from utils import get_json_file, save_json_file


class ConfigUI(BaseConfigUi):
    def __init__(self, farm: Farm, parent, main) -> None:
        self.farm = farm
        super().__init__(parent, main)

    def _create_poppup_screen(self, parent, main):
        super()._create_poppup_screen(parent, main)
        self.root.title('Config ' + self.farm.feature)

    def _save_config(self):
        self._do_save_config()
        cfg = get_json_file(CONFIG_FILE)
        cfg[self.farm.feature] = self.farm.cfg
        save_json_file(CONFIG_FILE, cfg)
        self.root.destroy()
