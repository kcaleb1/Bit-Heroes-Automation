from tkinter import CENTER, N, TOP, W, Tk, ttk, StringVar

from cv2 import Stitcher
from debug import save_print_dbg
from farm import Farm
from const import *
from utils import go_main_screen


class MainScreen():
    done = []
    done_btns = []
    queue = {}
    errors = []

    def __init__(self, farms: list) -> None:
        self.farms = farms

        self._create_root()
        self._create_main_screen()
        self._reset_config()

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
        # remove done buttons
        while len(self.done_btns):
            btn = self.done_btns.pop()
            if isinstance(btn, ttk.Button):
                btn.pack_forget()
        # reset queue
        for k in self.queue:
            self.queue[k].pack_forget()
        self.queue = {}
        for farm in self.farms:
            self._add_queue(farm)

    def _create_root(self):
        self.root = Tk()
        self.root.title('Bit Heroes Automation')
        self.root.geometry('450x380')
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._stop)

    def _create_main_screen(self):
        self._create_top_frame()
        self._create_errors_frame()
        self._create_queue_frame()
        self._create_done_frame()

    def _create_top_frame(self):
        self.top_fr = ttk.Frame(self.root)
        self.top_fr.grid(column=0, row=0, columnspan=3, sticky=W)
        self._setup_label()
        self._setup_button()

    def _setup_label(self):
        # label timer
        self.timer = 0
        self.timer_label = ttk.Label(self.top_fr, text='00:00:00')
        self.timer_label.grid(column=1, row=0)
        # frame to set max height
        fr = ttk.Frame(self.top_fr, height=50)
        fr.grid(column=1, row=1, sticky=N)
        # label farm
        self.txt_main_label = StringVar()
        self.main_label = ttk.Label(
            fr, textvariable=self.txt_main_label)
        self.main_label.pack()

    def _setup_button(self):
        self.start_enable = False
        # Start farm button
        self.start_btn = ttk.Button(
            self.top_fr, text="Start",
            command=self._start_farm, padding=10)
        # Stop farm button
        self.stop_btn = ttk.Button(
            self.top_fr, text="Stop",
            command=self._stop_farm, padding=10)
        self._start_stop_swap()

    def _create_queue_frame(self):
        ttk.Label(self.root, text='queue',
                  padding=(10, 0), background='#9e9e9e'
                  ).grid(column=1, row=1)
        self.queue_fr = ttk.Frame(self.root, padding=(10, 0))
        self.queue_fr.grid(column=1, row=2, sticky=N)

    def _add_queue(self, farm: Farm):
        self.queue[farm.feature] = ttk.Label(self.queue_fr, text=farm.feature)
        self.queue[farm.feature].pack(side=TOP)

    def _remove_queue(self, farm: Farm):
        self.queue.pop(farm.feature).pack_forget()

    def _create_errors_frame(self):
        ttk.Label(self.root, text='errors',
                  padding=(10, 0), background='#9e9e9e',
                  ).grid(column=2, row=1, columnspan=2, sticky=W)
        self.errors_fr = ttk.Frame(self.root, padding=(10, 0))
        self.errors_fr.grid(column=2, row=2, columnspan=2, sticky=N)

    def _create_done_frame(self):
        ttk.Label(self.root, text='done',
                  background='#9e9e9e', padding=(20, 0)
                  ).grid(column=0, row=1, sticky=W)
        self.done_fr = ttk.Frame(self.root)
        self.done_fr.grid(column=0, row=2, sticky=N)

    def _add_done_farm_btn(self, farm: Farm, farm_name: str):
        def _retry_done(btn: ttk.Button):
            self.done.remove(farm)
            self.farms.append(farm)
            self._add_queue(farm)
            btn.pack_forget()
            self.done_btns.remove(btn)

        b = ttk.Button(self.done_fr, text=farm_name,
                       command=lambda: _retry_done(b))
        self.done_btns.append(b)
        b.pack(side=TOP)

    def _create_error_frame_btn(self, farm: Farm, error: str):
        def _repaired_error(farm: Farm, fr: ttk.Frame):
            self.errors.remove(farm)
            self.farms.append(farm)
            self._add_queue(farm)
            fr.pack_forget()

        fr = ttk.Frame(self.errors_fr)
        fr.pack(side=TOP, anchor=W)

        ttk.Label(fr, text=error).grid(column=0, row=0, sticky=W)
        ttk.Button(fr, text='fixed',
                   command=lambda: _repaired_error(farm, fr)
                   ).grid(column=1, row=0, sticky=W)

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
                self._add_queue(self.farm)
            else:
                self._move_farm_done(type(self.farm), self.farm.feature)

        if len(self.farms) == 0:
            self._stop_farm()
            go_main_screen()
            return

        farm = self.farms.pop(0)
        self._remove_queue(farm)

        try:
            self.farm = farm()
        except Exception as ex:
            save_print_dbg(f'Failed to run {farm.feature}: {str(ex)}')
            self._move_farm_error(farm, ex)
            return self._next_farm()

        self.farm.start()
        self.txt_main_label.set(str(self.farm))

    def _move_farm_done(self, done: Farm, farm: str):
        self.done.append(done)
        self.farm = None
        self._add_done_farm_btn(done, farm)
        save_print_dbg(f'--- done: {self.done}')

    def _move_farm_error(self, farm: Farm, error: Exception):
        self.errors.append(farm)
        self.farm = None
        err = str(error)
        save_print_dbg(f'--- error:\n{err}')
        self._create_error_frame_btn(farm, err)

    def _stop_farm(self):
        save_print_dbg("**Stop farm")
        if self.farm != None:
            self.farm.stop()
            if type(self.farm) not in self.farms + self.done:
                self.farms.append(self.farm)
        self._reset_config()
        self._start_stop_swap()

    def _start_stop_swap(self):
        if self.start_enable:
            self.start_btn.grid_remove()
            self.stop_btn.grid(column=0, row=0,
                               rowspan=2, padx=10, pady=5)
            self.stop_btn.focus()
        else:
            self.start_btn.grid(column=0, row=0,
                                rowspan=2, padx=10, pady=5)
            self.stop_btn.grid_remove()
            self.start_btn.focus()
        self.start_enable = not self.start_enable
