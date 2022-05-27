from copy import copy
from tkinter.ttk import Frame, OptionMenu
from tkinter import W, Label, StringVar, Tk, IntVar


def create_option_menu(parent: Tk, data, value, name):
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
    OptionMenu(fr, var, *clone_data).grid(column=1, row=0)
    return var
