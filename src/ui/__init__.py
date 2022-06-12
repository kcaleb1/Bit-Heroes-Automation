from tkinter import Toplevel, ttk
from const import CONFIG_FILE
from utils import save_json_file


class BaseConfigUi:
    def __init__(self, parent, main) -> None:
        self._create_poppup_screen(parent, main)
        self._add_config_frames()
        self._add_save_button()

    def _create_poppup_screen(self, parent, main):
        window = Toplevel(parent)
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
        self.root.destroy()

    def _do_save_config(self):
        '''
        Inherit to do save action
        By update there own config into Farm.cfg
        '''
        pass
