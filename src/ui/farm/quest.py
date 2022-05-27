from copy import copy
from tkinter import W, Frame, Label, StringVar, IntVar
from tkinter.ttk import OptionMenu
from const import COSTS, DIFFICULTIES
from ui.farm import ConfigUI, Farm
from ui.farm.utils import create_option_menu

# TODO FIX THIS SHIT


class QuestConfigUI(ConfigUI):
    def __init__(self, farm: Farm, parent, main) -> None:
        super().__init__(farm, parent, main)

    def _add_config_frames(self):
        self.zone, self.floor = self._custom_zone_floor_option_menu(self.root)
        self.difficulty = create_option_menu(self.root,
                                             data=list(DIFFICULTIES.keys()),
                                             value=self.farm.difficulty,
                                             name='difficulty')

    def _do_save_config(self):
        self.farm.cfg['zone'] = self.zone.get()
        self.farm.cfg['floor'] = self.floor.get()
        self.farm.cfg['difficulty'] = self.difficulty.get()

    def _custom_zone_floor_option_menu(self, parent):
        def create_var(parent, value):
            clone_value = copy(value)
            if type(clone_value) == int:
                var = IntVar(master=parent, value=clone_value)
            elif type(clone_value) == str:
                var = StringVar(master=parent, value=clone_value)
            return var

        def update_floor(zone_selected, var_floor, opt_menu_floor):
            data = copy(self.farm.zones[zone_selected])
            var_floor.set(data[0])
            opt_menu_floor.set_menu(var_floor.get(), *data)

        # setup floor frame
        fr_floor = Frame(parent)
        Label(fr_floor, text='floor:', anchor=W).grid(column=0, row=0)
        clone_floor = copy(self.farm.zones[self.farm.zone])
        var_floor = create_var(fr_floor, self.farm.floor)
        clone_floor.insert(0, 0)  # insert empty value, to display whole data
        opt_menu_floor = OptionMenu(
            fr_floor, var_floor, *clone_floor)
        opt_menu_floor.grid(column=1, row=0)

        # setup zone frame
        fr_zone = Frame(parent)
        Label(fr_zone, text='zone:', anchor=W).grid(column=0, row=0)
        clone_zones = copy(list(self.farm.zones.keys()))
        var_zone = create_var(fr_zone, self.farm.zone)
        clone_zones.insert(0, 0)  # insert empty value, to display whole data
        OptionMenu(fr_zone, var_zone, *clone_zones,
                   command=lambda selected: update_floor(selected, var_floor,
                                                         opt_menu_floor)
                   ).grid(column=1, row=0)

        # let zone frame adding ahead of floor frame
        fr_zone.pack()
        fr_floor.pack()

        return var_zone, var_floor
