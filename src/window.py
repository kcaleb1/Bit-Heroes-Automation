import pyautogui
import pywinauto
import win32gui

import sys
from time import sleep
from debug import save_image
from const import *
from error import *


def get_app():
    global app
    app = pywinauto.Application().connect(path=APP_NAME)
    app.top_window().set_focus()


def click_screen_and_sleep(y, x, sleep_duration=SLEEP):
    app[GAME_TITLE].click_input(coords=(x, y + TITLE_BAR_HEIGHT))
    pyautogui.moveTo(y - y, x - x) # reset mouse position so not display unwanted UI
    sleep(sleep_duration)


def get_game_screen(game_title=GAME_TITLE):
    global x_multiply, y_multiply

    if sys.platform in ['Windows', 'win32', 'cygwin']:
        hwnd = win32gui.FindWindow(None, game_title)

        if not hwnd:
            raise MismatchConditionException(f'{game_title} not running')

        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        if x1 == MAX_RESOLUTION[0] and y1 == MAX_RESOLUTION[1]:
            pass
        elif x1 <= MAX_RESOLUTION[0] and y1 <= MAX_RESOLUTION[1]:
            x_multiply = x1 / MAX_RESOLUTION[0]
            y_multiply = y1 / MAX_RESOLUTION[1]
        else:
            raise MismatchConditionException('Resolution %s:%s not supported, working resolution is %s:%s and lower' %(x1, y1, *MAX_RESOLUTION))

        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        img = pyautogui.screenshot(region=(x, y, x1, y1))

        if DEBUG:
            save_image('get_game_screen', img)

        return img
    
    raise MismatchConditionException('OS not supported')


def press_escape():
    get_app()
    pywinauto.keyboard.send_keys('{VK_ESCAPE}')