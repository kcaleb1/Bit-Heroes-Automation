from copy import copy
from tkinter import W, Frame, Label, StringVar, IntVar
from tkinter.ttk import OptionMenu
from const import LIST_DIFFICULTIES
from ui.farm import ConfigUI, Farm
from ui.utils import create_option_menu


class QuestConfigUI(ConfigUI):
    def __init__(self, farm: Farm, parent, main) -> None:
        super().__init__(farm, parent, main)

    def _add_config_frames(self):
        self.zone, self.dungeon = self._custom_zone_dungeon_option_menu(
            self.root)
        self.difficulty = create_option_menu(self.root,
                                             data=LIST_DIFFICULTIES,
                                             value=self.farm.difficulty,
                                             name='difficulty')

    def _do_save_config(self):
        self.farm.cfg['zone'] = self.zone.get()
        self.farm.cfg['dungeon'] = self.dungeon.get()
        self.farm.cfg['difficulty'] = self.difficulty.get()

    def _custom_zone_dungeon_option_menu(self, parent):
        def create_var(parent, value):
            clone_value = copy(value)
            if type(clone_value) == int:
                var = IntVar(master=parent, value=clone_value)
            elif type(clone_value) == str:
                var = StringVar(master=parent, value=clone_value)
            return var

        def update_dungeon(zone_selected, var_dungeon, opt_menu_dungeon):
            data = copy(self.farm.zones[zone_selected])
            var_dungeon.set(data[0])
            opt_menu_dungeon.set_menu(var_dungeon.get(), *data)

        # setup dungeon frame
        fr_dungeon = Frame(parent)
        Label(fr_dungeon, text='dungeon:', anchor=W).grid(column=0, row=0)
        clone_dungeon = copy(self.farm.zones[self.farm.zone])
        var_dungeon = create_var(fr_dungeon, self.farm.dungeon)
        clone_dungeon.insert(0, 0)  # insert empty value, to display whole data
        opt_menu_dungeon = OptionMenu(
            fr_dungeon, var_dungeon, *clone_dungeon)
        opt_menu_dungeon.grid(column=1, row=0)

        # setup zone frame
        fr_zone = Frame(parent)
        Label(fr_zone, text='zone:', anchor=W).grid(column=0, row=0)
        clone_zones = copy(self.farm.list_zone)
        var_zone = create_var(fr_zone, self.farm.zone)
        clone_zones.insert(0, 0)  # insert empty value, to display whole data
        OptionMenu(fr_zone, var_zone, *clone_zones,
                   command=lambda selected: update_dungeon(selected, var_dungeon,
                                                           opt_menu_dungeon)
                   ).grid(column=1, row=0)

        # let zone frame adding ahead of dungeon frame
        fr_zone.pack()
        fr_dungeon.pack()

        return var_zone, var_dungeon
