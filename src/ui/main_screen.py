import os
from time import sleep
from tkinter import DISABLED, LEFT, N, NE, NW, TOP, W, PhotoImage, ttk, StringVar, Tk
from debug import print_stacktrace, save_print_dbg
from farm import Farm
from const import *
import const
from ui.config import CommonConfigUI
from ui.utils import add_tool_tip
from utils import \
    clean_config_of_farm, \
    find_image_and_click_then_sleep, \
    is_rerun_mode, \
    go_main_screen, \
    is_debug, \
    is_smart_rerun

GEAR_IMG = join(UI_IMAGE_PATH, 'gear-solid.png')
CONFIG_FILE_IMG = join(UI_IMAGE_PATH, 'file-pen-solid.png')
DEBUG_FILE_IMG = join(UI_IMAGE_PATH, 'file-alt-solid.png')
START_IMG = join(UI_IMAGE_PATH, 'play-solid.png')
STOP_IMG = join(UI_IMAGE_PATH, 'stop-solid.png')

IMG_SIZE = 28


class MainScreen():
    # pair 1
    farms = []
    queue = {}
    # pair 2
    done = []
    done_frames = {}

    errors = []

    start_btn_id = None
    timer_label_id = None

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
        self.check_run = []
        self.farm = None
        self.enable_rerun = False
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
        self._load_images()
        self._create_top_frame()
        self._create_errors_frame()
        self._create_queue_frame()
        self._create_done_frame()

    def _load_images(self):
        self.gear_img = PhotoImage(file=GEAR_IMG).subsample(IMG_SIZE, IMG_SIZE)

        self.config_file_img = PhotoImage(
            file=CONFIG_FILE_IMG).subsample(IMG_SIZE, IMG_SIZE)
        self.debug_file_img = PhotoImage(
            file=DEBUG_FILE_IMG).subsample(IMG_SIZE, IMG_SIZE)

        self.start_img = PhotoImage(file=START_IMG).subsample(22, 22)
        self.stop_img = PhotoImage(file=STOP_IMG).subsample(22, 22)

    def _create_top_frame(self):
        top_fr = ttk.Frame(self.root)
        top_fr.grid(column=0, row=0, columnspan=3, sticky=W)
        self._setup_label(top_fr)
        self._setup_button(top_fr)
        self._utilities_button(top_fr)

    def _utilities_button(self, top_fr: ttk.Frame):
        fr = ttk.Frame(top_fr, padding=(10, 0, 0, 7))
        fr.grid(column=0, row=2, sticky=W)

        self._add_common_config_button(fr).pack(side=LEFT)
        self._add_open_config_file_button(fr).pack(side=LEFT)
        self._add_open_debug_file_button(fr).pack(side=LEFT)

    def _add_common_config_button(self, top_fr: ttk.Frame) -> ttk.Button:
        def open_edit_common_config():
            CommonConfigUI(self.root, self)

        btn = ttk.Button(top_fr, image=self.gear_img,
                         command=open_edit_common_config)
        add_tool_tip(btn, "Common configuration")
        return btn

    def _add_open_config_file_button(self, top_fr: ttk.Frame) -> ttk.Button:
        def open_config_file():
            os.startfile(CONFIG_FILE, 'open')

        btn = ttk.Button(top_fr, image=self.config_file_img,
                         command=open_config_file)
        add_tool_tip(btn, "Open config file")
        return btn

    def _add_open_debug_file_button(self, top_fr: ttk.Frame) -> ttk.Button:
        def open_debug_file():
            if is_debug and os.path.exists(DEBUG_TEXT_PATH):
                os.startfile(DEBUG_TEXT_PATH, 'open')

        btn = ttk.Button(top_fr, image=self.debug_file_img,
                         command=open_debug_file)
        add_tool_tip(btn, "Open debug file")
        return btn

    def _setup_label(self, top_fr: ttk.Frame):
        # label timer
        self.timer = 0
        self.timer_label = ttk.Label(top_fr, text='00:00:00')
        self.timer_label.grid(column=1, row=0, sticky=W)
        add_tool_tip(self.timer_label, "Total run time")
        # frame to set max height
        fr = ttk.Frame(top_fr, height=50)
        fr.grid(column=1, rowspan=2, row=1, sticky=N)
        # label farm
        self.txt_main_label = StringVar()
        self.main_label = ttk.Label(
            fr, textvariable=self.txt_main_label)
        self.main_label.pack()
        add_tool_tip(self.main_label, "Farm information")

    def _setup_button(self, top_fr: ttk.Frame):
        self.start_enable = False
        # Start farm button
        pad = (30, 10)
        self.start_btn = ttk.Button(
            top_fr, image=self.start_img,
            command=self._start_farm, padding=pad)
        add_tool_tip(self.start_btn, "Start farming")
        # Stop farm button
        self.stop_btn = ttk.Button(
            top_fr, image=self.stop_img,
            command=self._stop_farm, padding=pad)
        add_tool_tip(self.stop_btn, "Stop farming")
        self._start_stop_swap()

    def _create_queue_frame(self):
        def move_queue_to_done():
            while len(self.farms):
                f = self.farms.pop(0)
                self._add_done_farm_btn(f)
                self._remove_queue(f)

        fr = ttk.Frame(self.root)
        fr.grid(column=1, row=1)
        btn = ttk.Button(fr, text='<<<',
                         command=lambda: move_queue_to_done(),
                         padding=(-22, -2)
                         )
        btn.pack(side=LEFT)
        add_tool_tip(btn, "Move all to done")
        lb = ttk.Label(fr, text='queue',
                       padding=(5, 0, 26, 0),
                       background='#9e9e9e',
                       )
        lb.pack(side=LEFT)
        add_tool_tip(lb, 'Execute order')
        #
        self.queue_fr = ttk.Frame(self.root, padding=(10, 0))
        self.queue_fr.grid(column=1, row=2, sticky=N)

    def _add_queue_and_farms(self, farm: Farm):
        if farm in self.queue:
            return

        if farm not in self.farms:
            self.farms.append(farm)

        if farm in self.check_run:
            self.check_run.remove(farm)

        def move_to_done():
            self.farms.remove(farm)
            self._remove_queue(farm)
            self._add_done_farm_btn(farm)

        fr = ttk.Frame(self.queue_fr)
        fr.pack(side=TOP, anchor=NW)
        btn = ttk.Button(fr, text='<<',
                         command=lambda: move_to_done(),
                         padding=(-22, -2)
                         )
        btn.pack(side=LEFT)
        add_tool_tip(btn, "Move to done")
        self._create_config_button(fr, farm)
        self.queue[farm] = fr

    def _remove_queue(self, farm: Farm):
        if farm in self.farms:
            self.farms.remove(farm)
        self.queue.pop(farm).pack_forget()

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
                self.done_frames.pop(f).pack_forget()

        fr = ttk.Frame(self.root)
        fr.grid(column=0, row=1, sticky=W)

        lb = ttk.Label(fr, text='done',
                       background='#9e9e9e', padding=(26, 0, 5, 0)
                       )
        lb.pack(side=LEFT)
        add_tool_tip(lb, 'Not execute')
        btn = ttk.Button(fr, text='>>>',
                         command=lambda: move_done_to_queue(),
                         padding=(-22, -2)
                         )
        btn.pack(side=LEFT)
        add_tool_tip(btn, "Move all to queue")

        self.done_fr = ttk.Frame(self.root)
        self.done_fr.grid(column=0, row=2, sticky=N)

    def _add_done_farm_btn(self, farm: Farm):
        def move_to_queue():
            self.done.remove(farm)
            self._add_queue_and_farms(farm)
            self.done_frames.pop(farm).pack_forget()

        fr = ttk.Frame(self.done_fr)
        fr.pack(side=TOP, anchor=NE)
        self._create_config_button(fr, farm)
        btn = ttk.Button(fr, text='>>',
                         command=lambda: move_to_queue(),
                         padding=(-22, -2)
                         )
        btn.pack(side=LEFT)
        add_tool_tip(btn, "Move to queue")
        if farm not in self.done:
            self.done.append(farm)
        self.done_frames[farm] = fr

    def _create_error_frame_btn(self, farm: Farm, error: str):
        def _repaired_error(farm: Farm, fr: ttk.Frame):
            clean_config_of_farm(farm.feature)
            self.try_create_farm(farm).set_default_config()
            self.errors.remove(farm)
            self._add_queue_and_farms(farm)
            fr.pack_forget()

        fr = ttk.Frame(self.errors_fr)
        fr.pack(side=TOP, anchor=N)

        btn = ttk.Button(fr, text='<<',
                         padding=(-22, 10),
                         command=lambda: _repaired_error(farm, fr),
                         )
        btn.pack(anchor=W, side=LEFT)
        add_tool_tip(btn, 'Move back to queue with default config')
        ttk.Label(fr, text=error, wraplength=160,
                  width=160).pack(anchor=W, side=LEFT)

    def _start_farm(self):
        if self.farms == None or len(self.farms) == 0 or isinstance(self.farms, Farm):
            raise Exception('Empty farms')
        self._start_stop_swap()
        self._update_timer()
        self._do_farm()

    def _do_farm(self):
        if self.start_enable:
            return

        if self.farm == None or self.farm.is_done():
            self.try_reconnect = 0
            self._next_farm()
        elif self.farm.get_run_time() > TRIGGER_RECONNECT_CHECK + (self.try_reconnect * FIVE_MINUTE):
            def reconnect():
                find_image_and_click_then_sleep(COMMON_RECONNECT)
                self.farm.stop()
                sleep(5)
                reconnect()

            self.try_reconnect += 1
            old_dbg = const.dbg_name
            const.dbg_name = 'reconnect'
            try:
                reconnect()
            except:
                pass
            const.dbg_name = old_dbg

        self.set_main_label_by_farm()
        self.start_btn_id = self.start_btn.after(SECOND_MS, self._do_farm)

    def _update_timer(self):
        if self.start_enable:
            return

        self.timer += 1
        h = int(self.timer / 3600)
        m = int((self.timer - h * 3600) / 60)
        s = int(self.timer - h * 3600 - m * 60)
        self.timer_label.configure(text=f'{h:02d}:{m:02d}:{s:02d}')

        self.timer_label_id = self.timer_label.after(
            SECOND_MS, self._update_timer)

    def _next_farm(self):
        if self.farm:
            f = type(self.farm)
            if self.farm.get_result():
                self._add_queue_and_farms(f)
                self.check_run.append(f)
            else:
                err = self.farm.get_error()
                if err == '':
                    self._move_farm_done(f)
                else:
                    self._move_farm_to_error(f, Exception(err))

        if len(self.farms) == 0:
            self._stop_farm()
            go_main_screen()
            return

        farm = self.farms.pop(0)
        self._remove_queue(farm)

        self.farm = self.try_create_farm(farm)
        if not self.farm:
            return self._next_farm()

        self.farm.rerun_mode = self.check_smart_rerun(farm)
        self.farm.start()
        self.set_main_label_by_farm()

    def check_smart_rerun(self, farm: Farm) -> bool:
        if not is_smart_rerun():
            return is_rerun_mode()

        self.check_run.append(farm)
        self.check_run = list(dict.fromkeys(self.check_run))

        for q in self.queue:
            if q not in self.check_run:
                return False
        return True

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
        save_print_dbg(f'--- done: {[x.feature for x in self.done]}')

    def _move_farm_to_error(self, farm: Farm, error: Exception):
        if farm in self.queue:
            self._remove_queue(farm)

        self.errors.append(farm)
        self.farm = None
        err = str(error)
        save_print_dbg(f'--- error:\n{err}')
        self._create_error_frame_btn(farm, err)

    def _stop_farm(self):
        save_print_dbg("**Stop farm")
        self._stop_schedule_events()
        if self.farm != None:
            self.farm.stop()
            if type(self.farm) not in self.farms + self.done:
                self.farms.append(type(self.farm))
        self._reset_config()
        self._start_stop_swap()

    def _stop_schedule_events(self):
        events = {
            self.start_btn: self.start_btn_id,
            self.timer_label: self.timer_label_id
        }

        for k, v in events.items():
            try:
                k.after_cancel(v)
            except:
                pass

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
            btn = ttk.Button(parent, text=farm.feature,
                             padding=(0, -2),
                             state=DISABLED)
            add_tool_tip(btn, f"No configuration for {farm.feature}")
        else:
            btn = ttk.Button(parent, text=farm.feature,
                             padding=(0, -2),
                             command=lambda: btn_cmd())
            add_tool_tip(btn, f"Open {farm.feature} configuration")
        btn.pack(side=LEFT)

    def set_main_label_by_farm(self):
        self.txt_main_label.set(
            self.farm.__str__() if self.farm else 'Nothing')
