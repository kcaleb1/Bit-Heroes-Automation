import json
from tkinter import Toplevel, ttk
from const import CONFIG_FILE
from farm import Farm


class ConfigUI():
    def __init__(self, farm: Farm, parent, main) -> None:
        self.farm = farm
        self._create_poppup_screen(parent, main)
        self._add_config_frames()
        self._add_save_button()

    def _create_poppup_screen(self, parent, main):
        window = Toplevel(parent)
        window.title('Config ' + self.farm.feature)
        pos = main.get_root_pos()
        window.geometry(f"270x130+{pos[0]}+{pos[1]}")
        window.grab_set()  # for disable main window
        window.focus()
        window.resizable(False, False)

        self.root = window

    def _add_config_frames(self):
        '''
        Inherit to do add config farms
        Use pack() only
        '''
        pass

    def _add_save_button(self):
        ttk.Button(self.root,
                   text='Save',
                   command=self._save_config).pack(pady=5)

    def _save_config(self):
        self._do_save_config()
        cfg = {}
        with open(CONFIG_FILE, 'r') as f:
            cfg = json.load(f)
        cfg[self.farm.feature] = self.farm.cfg
        with open(CONFIG_FILE, 'w') as f:
            f.write(json.dumps(cfg, indent=4))
        self.root.destroy()

    def _do_save_config(self):
        '''
        Inherit to do save action
        By update there own config into Farm.cfg
        '''
        pass
