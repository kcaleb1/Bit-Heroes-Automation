from tkinter import Tk, ttk, StringVar
from debug import save_print_dbg
from farm import Farm
from const import *
from utils import go_main_screen


class MainScreen():
    done = []
    errors = []

    def __init__(self, farms: list) -> None:
        self._create_root()
        self._create_main_screen()
        self._reset_config()
        self.farms = farms

    def display(self):
        save_print_dbg('**Start app')
        self.root.mainloop()

    def _stop(self):
        save_print_dbg("**Stop app")
        self._stop_farm()
        self.root.quit()

    def _reset_config(self):
        self.is_stop = False
        self.process = None
        self.farm = None
        if self.done and self.done != []:
            self.farms += self.done
        self.done = []
        self.txt_main_label.set('Nothing')

    def _create_root(self):
        self.root = Tk()
        self.root.title('Bit Heroes Automation')
        self.root.geometry('450x350')
        self.root.resizable(None, None)
        self.root.protocol("WM_DELETE_WINDOW", self._stop)

    def _create_main_screen(self):
        self.top_fr = ttk.Frame(self.root, padding=10)
        self.top_fr.pack()
        self._setup_label()
        self._setup_button()

    def _repaired_error(self, farm: Farm, fr: ttk.Frame):
        self.errors.remove(farm)
        self.farms.append(farm)
        fr.pack_forget()

    def _create_error_frame(self, farm: Farm, error: str):
        fr = ttk.Frame(self.root, border=1)
        fr.pack()

        ttk.Label(fr, text=error).grid(column=0, row=0)
        ttk.Button(fr, text='repaired',
                   command=lambda: self._repaired_error(farm, fr)
                   ).grid(column=1, row=0)

    def _setup_label(self):
        # label timer
        self.timer = 0
        self.timer_label = ttk.Label(self.top_fr, text='00:00:00')
        self.timer_label.grid(column=1, row=0)
        # label farm
        self.txt_main_label = StringVar()
        self.main_label = ttk.Label(
            self.top_fr, textvariable=self.txt_main_label)
        self.main_label.grid(column=1, row=1)

    def _setup_button(self):
        self.start_enable = True
        # Start farm button
        self.start_btn = ttk.Button(
            self.top_fr, text="Start", command=self._start_farm)
        self.start_btn.grid(column=1, row=2)
        self.start_btn.focus()
        # Stop farm button
        self.stop_btn = ttk.Button(
            self.top_fr, text="Stop", command=self._stop_farm)

    def _start_farm(self):
        if self.farms == None or len(self.farms) == 0 or isinstance(self.farms, Farm):
            raise Exception('Invalid object')
        self._reset_config()
        self._start_stop_swap()
        self._do_farm()

    def _do_farm(self):
        if self.start_enable:
            return

        self._update_timer()

        if self.farm == None or self.farm.is_done():
            self._next_farm()
        self.start_btn.after(1000, self._do_farm)

    def _update_timer(self):
        # update timer
        self.timer += 1
        h = int(self.timer / 3600)
        m = int((self.timer - h * 3600) / 60)
        s = int(self.timer - h * 3600 - m * 60)
        self.timer_label.configure(text=f'{h:02d}:{m:02d}:{s:02d}')

    def _next_farm(self):
        if self.farm != None:
            if self.farm.get_result():
                self.farms.append(type(self.farm))
            else:
                self._move_farm_done(type(self.farm))

        if len(self.farms) == 0:
            self._stop_farm()
            go_main_screen()
            return

        farm = self.farms.pop(0)

        try:
            self.farm = farm()
        except Exception as ex:
            save_print_dbg(f'Failed to run {farm}: {str(ex)}')
            self._move_farm_error(farm, ex)
            return self._next_farm()

        self.farm.start()
        self.txt_main_label.set(str(self.farm))

    def _move_farm_done(self, done: Farm):
        self.done.append(done)
        self.farm = None
        save_print_dbg(f'--- done: {self.done}')

    def _move_farm_error(self, farm: Farm, error: Exception):
        self.errors.append(farm)
        self.farm = None
        err = str(error)
        save_print_dbg(f'--- error:\n{err}')
        self._create_error_frame(farm, err)

    def _stop_farm(self):
        save_print_dbg("**Stop farm")
        if self.farm != None:
            self.farm.stop()
        self._reset_config()
        self._start_stop_swap()

    def _start_stop_swap(self):
        if self.start_enable:
            self.start_btn.grid_remove()
            self.stop_btn.grid(column=1, row=2)
            self.stop_btn.focus()
        else:
            self.start_btn.grid(column=1, row=2)
            self.stop_btn.grid_remove()
            self.start_btn.focus()
        self.start_enable = not self.start_enable
