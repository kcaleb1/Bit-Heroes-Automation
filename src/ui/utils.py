from copy import copy
from tkinter.ttk import Frame, OptionMenu, Checkbutton
from tkinter import E, LEFT, W, BooleanVar, Label, StringVar, Tk, IntVar
from idlelib.tooltip import Hovertip


def create_option_menu(parent: Tk, data, value, name, tooltip=None):
    fr = Frame(parent)
    fr.pack()
    Label(fr, text=f'{name}:', anchor=W).grid(column=0, row=0)
    clone_data = copy(data)
    clone_value = copy(value)
    if type(value) == int:
        var = IntVar(master=fr, value=clone_value)
    elif type(value) == str:
        var = StringVar(master=fr, value=clone_value)
    clone_data.insert(0, 0)  # insert empty value, to display whole data
    opt = OptionMenu(fr, var, *clone_data)
    opt.grid(column=1, row=0)
    if tooltip:
        add_tool_tip(opt, tooltip)

    return var


def create_check_button(parent: Tk, value, name, tooltip=None):
    fr = Frame(parent, width=30)
    fr.pack()
    var = BooleanVar(master=fr, value=value)
    btn = Checkbutton(fr, text=name, variable=var,
                      width=15, padding=(10, 0, 0, 0))
    btn.pack(side=LEFT, anchor=E)
    if tooltip:
        add_tool_tip(btn, tooltip)
    return var


def add_tool_tip(object, msg):
    Hovertip(object, msg)
