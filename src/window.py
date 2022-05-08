import pyautogui
import pywinauto
import win32gui

import sys
from time import sleep
from debug import save_image_dbg
from error import *
from const import *
import const


def get_app():
    const.app = pywinauto.Application().connect(path=APP_NAME)
    const.app.top_window().set_focus()


def click_screen_and_sleep(y: int, x: int, sleep_duration=SLEEP):
    cur_pos = pyautogui.position()
    const.app[GAME_TITLE].click_input(coords=(x, y + TITLE_BAR_HEIGHT))
    # reset mouse position so not display unwanted UI
    pyautogui.moveTo(cur_pos.x, cur_pos.y)
    sleep(sleep_duration)


def get_game_screen(game_title=GAME_TITLE):
    global x_multiply, y_multiply

    if sys.platform in ['Windows', 'win32', 'cygwin']:
        hwnd = win32gui.FindWindow(None, game_title)

        if not hwnd:
            raise MismatchConditionException(txt=f'{game_title} not running')

        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        if x1 == MAX_RESOLUTION[0] and y1 == MAX_RESOLUTION[1]:
            pass
        elif x1 <= MAX_RESOLUTION[0] and y1 <= MAX_RESOLUTION[1]:
            const.x_multiply = x1 / MAX_RESOLUTION[0]
            const.y_multiply = y1 / MAX_RESOLUTION[1]
        else:
            raise MismatchConditionException(
                txt='Resolution %s:%s not supported, working resolution is %s:%s and lower' % (x1, y1, *MAX_RESOLUTION))

        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        img = pyautogui.screenshot(region=(x, y, x1, y1))

        # save_image_dbg('get_game_screen', img)

        return img

    raise MismatchConditionException(txt='OS not supported')


def press_escape():
    get_app()
    pywinauto.keyboard.send_keys('{VK_ESCAPE}')
