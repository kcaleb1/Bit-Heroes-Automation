from const import CONFIG_FILE, DEBUG_TEXT_PATH, LIST_COSTS, SAVE_DEBUG_PATH
import const
from ui import BaseConfigUi
from ui.utils import create_check_button, create_option_menu
from utils import get_json_file, is_decline_treasure, is_rerun_mode, is_debug, is_save_captured_image, is_smart_rerun, is_brush_force_energy, save_json_file


class CommonConfigUI(BaseConfigUi):
    def __init__(self, parent, main) -> None:
        super().__init__(parent, main)
        self.root.geometry(f"270x180")

    def _create_poppup_screen(self, parent, main):
        super()._create_poppup_screen(parent, main)
        self.root.title('Common config')

    def _add_config_frames(self):
        self.debug = create_check_button(self.root, is_debug(),
                                         'Debug',
                                         f'Save debug into file {DEBUG_TEXT_PATH}')
        self.save_captured_image = create_check_button(
            self.root, is_save_captured_image(),
            'Save image',
            'Save image when running tool, for debug only\n'
            'Might increasing disk space\n'
            f'Image store location: {SAVE_DEBUG_PATH}')
        self.rerun = create_check_button(self.root, is_rerun_mode(),
                                         'Rerun',
                                         'Enable: continuously run farm until it ran out of energy\n'
                                         'Disable: run each mode 1 by 1')
        self.smart_rerun = create_check_button(
            self.root, is_smart_rerun(), 'Smart rerun',
            'Run each mode 1 by 1 in first run\n'
            'And then run each mode until ran out of energy \n'
            'Only work when rerun enabled')
        self.brush_force_energy = create_check_button(
            self.root, is_brush_force_energy(), 'Brush force energy',
            'Rerun by use highest energy and then decrease when got not enough energy until 1\n'
            'This will ignore the cost configuration\n'
            'Only work when rerun enabled')
        self.decline_treasure = create_check_button(
            self.root, is_decline_treasure(), 'Decline treasure')
        self.cost = create_option_menu(
            self.root, [0] + LIST_COSTS, 0, 'Set all farm cost', 'Except 0')

    def _do_save_config(self):
        cfg = get_json_file(CONFIG_FILE)
        cfg['debug'] = self.debug.get()
        const.DEBUG = cfg['debug']
        cfg['save_captured_image'] = self.save_captured_image.get()
        const.DEBUG_SAVE_IMG = cfg['save_captured_image']
        cfg['rerun_mode'] = self.rerun.get()
        cfg['smart_rerun_mode'] = self.smart_rerun.get()
        cfg['brush_force_energy'] = self.brush_force_energy.get()
        cfg['decline_treasure'] = self.decline_treasure.get()

        # set all cost of farm, except 0
        cost = self.cost.get()
        if cost:
            for k, v in cfg.items():
                if type(v) is dict and 'cost' in v:
                    cfg[k]['cost'] = cost

        save_json_file(CONFIG_FILE, cfg)
