from multiprocessing import Process
import multiprocessing
from time import sleep
from tkinter import Tk, ttk, StringVar
from debug import save_print_dbg

from farm import Farm
from const import *


class MainScreen():
    def __init__(self, farms: list) -> None:
        self._create_root()
        self._create_main_frame()
        self._reset_config()
        self.farms = farms

    def display(self):
        save_print_dbg('**Start app')
        self.root.mainloop()

    def stop(self):
        save_print_dbg("**Stop app")
        self._stop_farm()
        self.root.quit()

    def _reset_config(self):
        self.is_stop = False
        self.process = None
        self.farm = None
        self.done = []
        self.txt_main_label.set('Nothing')

    def _create_root(self):
        self.root = Tk()
        self.root.title('Bit Heroes Automation')
        self.root.geometry('300x150')
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.stop)

    def _create_main_frame(self):
        # self.main_frame = ttk.Frame(self.root, padding=10)
        # self.main_frame.grid()

        self._setup_label()
        self._setup_button()

    def _setup_label(self):
        self.txt_main_label = StringVar()
        self.main_label = ttk.Label(
            self.root, textvariable=self.txt_main_label)
        # self.main_label.grid(column=0, row=1)
        self.main_label.pack()

    def _setup_button(self):
        self.start_enable = True
        # Start farm button
        self.start_btn = ttk.Button(
            self.root, text="Start", command=self._start_farm)
        self.start_btn.pack()
        self.start_btn.focus()
        # Stop farm button
        self.stop_btn = ttk.Button(
            self.root, text="Stop", command=self._stop_farm)

    def _start_farm(self):
        if self.farms == None or len(self.farms) == 0 or isinstance(self.farms, Farm):
            raise Exception('Invalid object')
        self._reset_config()
        self._start_stop_swap()
        self._do_farm()

    def _do_farm(self):
        if self.start_enable:
            return
        if self.farm == None or self.farm.is_done():
            self._next_farm()
        self.start_btn.after(1000, self._do_farm)

    def _next_farm(self):
        if len(self.done) >= len(self.farms):
            self._stop_farm()
            return

        if self.farm != None and not self.farm.get_result():
            self.done.append(type(self.farm))
            save_print_dbg(f'--- done: {self.done}')

        while True:
            farm = self.farms.pop(0)
            self.farms.append(farm)

            if farm not in self.done:
                break

        self.farm = farm()
        self.farm.start()

        self.txt_main_label.set(str(self.farm))

    def _stop_farm(self):
        if self.farm != None:
            save_print_dbg("**Stop farm")
            self.farm.stop()
            self._reset_config()
            self.done = self.farms
            self._start_stop_swap()

    def _start_stop_swap(self):
        if self.start_enable:
            self.start_btn.pack_forget()
            self.stop_btn.pack()
            self.stop_btn.focus()
        else:
            self.start_btn.pack()
            self.stop_btn.pack_forget()
            self.start_btn.focus()
        self.start_enable = not self.start_enable
