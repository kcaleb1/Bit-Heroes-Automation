import pyautogui
import pywinauto
import win32gui

import sys
from time import sleep
from debug import save_image_dbg, save_print_dbg
from error import *
from const import *
import const


def get_app():
    const.app = pywinauto.Application().connect(path=APP_NAME)
    const.app.top_window().set_focus()


def click_screen_and_sleep(y: int, x: int, sleep_duration=SLEEP):
    def add(x): return x + PREFIX_CLICK
    cur_active = pyautogui.getActiveWindow()
    cur_pos = pyautogui.position()
    const.app[GAME_TITLE].click_input(
        coords=(add(x), add(y) + TITLE_BAR_HEIGHT))
    # reset mouse position and set focus to previous app
    pyautogui.moveTo(cur_pos.x, cur_pos.y)
    cur_active.activate()
    sleep(sleep_duration)


def get_game_screen(game_title=GAME_TITLE):
    global x_multiply, y_multiply

    if sys.platform in ['Windows', 'win32', 'cygwin']:
        # if not const.hwnd:
        const.hwnd = win32gui.FindWindow(None, game_title)

        if not const.hwnd:
            raise MismatchConditionException(txt=f'{game_title} not running')

        x, y, x1, y1 = win32gui.GetClientRect(const.hwnd)
        if x1 == MAX_RESOLUTION[0] and y1 == MAX_RESOLUTION[1]:
            pass
        # elif x1 <= MAX_RESOLUTION[0] and y1 <= MAX_RESOLUTION[1]:
        #     const.x_multiply = x1 / MAX_RESOLUTION[0]
        #     const.y_multiply = y1 / MAX_RESOLUTION[1]
        #     save_print_dbg(f'*current_resolution: {x1}:{y1}')
        #     save_print_dbg(f'*max_resolution:     {MAX_RESOLUTION}')
        else:
            raise MismatchConditionException(
                txt='Resolution %s:%s not supported, working resolution is %s:%s' % (x1, y1, *MAX_RESOLUTION))

        x, y = win32gui.ClientToScreen(const.hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(const.hwnd, (x1 - x, y1 - y))
        const.app_pos = (x, y, x1, y1)

        img = pyautogui.screenshot(region=const.app_pos)

        # save_image_dbg('get_game_screen', img)

        return img

    raise MismatchConditionException(txt='OS not supported')


def press_escape():
    cur_active = pyautogui.getActiveWindow()
    get_app()
    pywinauto.keyboard.send_keys('{VK_ESCAPE}')
    save_print_dbg('pressed escape')
    cur_active.activate()
