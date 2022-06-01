from tkinter import DISABLED, LEFT, N, NE, NW, TOP, W, Tk, ttk, StringVar
from debug import save_print_dbg
from farm import Farm
from const import *
import const
from ui.farm import ConfigUI
from utils import find_image_and_click_then_sleep, go_main_screen


class MainScreen():
    # pair 1
    farms = []
    queue = {}
    # pair 2
    done = []
    done_frames = {}

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
        self.farm = None
        self.txt_main_label.set('Nothing')
        # reset queue
        for k in self.queue:
            self.queue[k].pack_forget()
        self.queue = {}
        for farm in self.farms:
            self._add_queue_and_farms(farm)

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
        def move_queue_to_done():
            while len(self.farms):
                f = self.farms.pop(0)
                self._add_done_farm_btn(f)
                self._remove_queue(f)

        fr = ttk.Frame(self.root)
        fr.grid(column=1, row=1)
        ttk.Button(fr, text='<<<',
                   command=lambda: move_queue_to_done(),
                   padding=(-22, -2)
                   ).pack(side=LEFT)
        ttk.Label(fr, text='queue',
                  padding=(5, 0, 26, 0), background='#9e9e9e'
                  ).pack(side=LEFT)
        #
        self.queue_fr = ttk.Frame(self.root, padding=(10, 0))
        self.queue_fr.grid(column=1, row=2, sticky=N)

    def _add_queue_and_farms(self, farm: Farm):
        if farm.feature in self.queue:
            return

        if farm not in self.farms:
            self.farms.append(farm)

        def move_to_done():
            self.farms.remove(farm)
            self._remove_queue(farm)
            self._add_done_farm_btn(farm)

        fr = ttk.Frame(self.queue_fr)
        fr.pack(side=TOP, anchor=NW)
        ttk.Button(fr, text='<<',
                   command=lambda: move_to_done(),
                   padding=(-22, -2)
                   ).pack(side=LEFT)
        self._create_config_button(fr, farm)
        self.queue[farm.feature] = fr

    def _remove_queue(self, farm: Farm):
        if farm in self.farms:
            self.farms.remove(farm)
        self.queue.pop(farm.feature).pack_forget()

    def _create_errors_frame(self):
        ttk.Label(self.root, text='errors',
                  padding=(26, 0), background='#9e9e9e',
                  ).grid(column=2, row=1, columnspan=2, sticky=W)
        self.errors_fr = ttk.Frame(self.root, padding=(10, 0))
        self.errors_fr.grid(column=2, row=2, columnspan=2, sticky=N)

    def _create_done_frame(self):
        def move_done_to_queue():
            while len(self.done):
                f = self.done.pop(0)
                self._add_queue_and_farms(f)
                self.done_frames.pop(f.feature).pack_forget()

        fr = ttk.Frame(self.root)
        fr.grid(column=0, row=1, sticky=W)

        ttk.Label(fr, text='done',
                  background='#9e9e9e', padding=(26, 0, 5, 0)
                  ).pack(side=LEFT)
        ttk.Button(fr, text='>>>',
                   command=lambda: move_done_to_queue(),
                   padding=(-22, -2)
                   ).pack(side=LEFT)

        self.done_fr = ttk.Frame(self.root)
        self.done_fr.grid(column=0, row=2, sticky=N)

    def _add_done_farm_btn(self, farm: Farm):
        def move_to_queue():
            self.done.remove(farm)
            self._add_queue_and_farms(farm)
            self.done_frames.pop(farm.feature).pack_forget()

        fr = ttk.Frame(self.done_fr)
        fr.pack(side=TOP, anchor=NE)
        self._create_config_button(fr, farm)
        ttk.Button(fr, text='>>',
                   command=lambda: move_to_queue(),
                   padding=(-22, -2)
                   ).pack(side=LEFT)
        if farm not in self.done:
            self.done.append(farm)
        self.done_frames[farm.feature] = fr

    def _create_error_frame_btn(self, farm: Farm, error: str):
        def _repaired_error(farm: Farm, fr: ttk.Frame):
            self.errors.remove(farm)
            self._add_queue_and_farms(farm)
            fr.pack_forget()

        fr = ttk.Frame(self.errors_fr)
        fr.pack(side=TOP, anchor=W)

        ttk.Label(fr, text=error).pack(anchor=W)
        ttk.Button(fr, text='fixed',
                   command=lambda: _repaired_error(farm, fr)
                   ).pack(anchor=W)

    def _start_farm(self):
        if self.farms == None or len(self.farms) == 0 or isinstance(self.farms, Farm):
            raise Exception('Empty farms')
        self._start_stop_swap()
        self._do_farm()

    def _do_farm(self):
        if self.start_enable:
            return

        self._update_timer()

        if self.farm == None or self.farm.is_done():
            self._next_farm()
        elif self.farm.get_run_time() > TRIGGER_RECONNECT_CHECK:
            self.farm.stop()
            const.dbg_name = 'reconnect'
            while not self.start_enable:
                try:
                    find_image_and_click_then_sleep(
                        COMMON_RECONNECT, retry_time=20)
                except:
                    break

        self.start_btn.after(1000, self._do_farm)

    def _update_timer(self):
        self.timer += 1
        h = int(self.timer / 3600)
        m = int((self.timer - h * 3600) / 60)
        s = int(self.timer - h * 3600 - m * 60)
        self.timer_label.configure(text=f'{h:02d}:{m:02d}:{s:02d}')

    def _next_farm(self):
        if self.farm != None:
            if self.farm.get_result():
                self._add_queue_and_farms(type(self.farm))
            else:
                self._move_farm_done(type(self.farm))

        if len(self.farms) == 0:
            self._stop_farm()
            go_main_screen()
            return

        farm = self.farms.pop(0)
        self._remove_queue(farm)

        self.farm = self.try_create_farm(farm)
        if not self.farm:
            return self._next_farm()

        self.farm.start()
        self.txt_main_label.set(str(self.farm))

    def try_create_farm(self, farm: Farm):
        try:
            return farm()
        except Exception as ex:
            save_print_dbg(f'Failed to create {farm.feature}: {str(ex)}')
            self._move_farm_to_error(farm, ex)
            return None

    def _move_farm_done(self, done: Farm):
        self.done.append(done)
        self.farm = None
        self._add_done_farm_btn(done)
        save_print_dbg(f'--- done: {self.done}')

    def _move_farm_to_error(self, farm: Farm, error: Exception):
        if farm.feature in self.queue:
            self._remove_queue(farm)

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
                self.farms.append(type(self.farm))
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

    def get_root_pos(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        return (x, y)

    def _create_config_button(self, parent, farm: Farm):
        def btn_cmd():
            f = self.try_create_farm(farm)
            if not f:
                return
            f.show_config_ui(parent, self)

        if farm.configUI == None:
            t = ttk.Button(parent, text=farm.feature,
                           padding=(0, -2),
                           state=DISABLED)
        else:
            t = ttk.Button(parent, text=farm.feature,
                           padding=(0, -2),
                           command=lambda: btn_cmd())
        t.pack(side=LEFT)
