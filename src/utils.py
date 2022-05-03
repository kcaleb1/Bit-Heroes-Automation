from http.client import EXPECTATION_FAILED
from PIL import Image, ImageGrab
import numpy as np
import cv2
import pyautogui
import win32gui
import pywinauto
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

import os
import sys

GAME_TITLE='Bit Heroes'
APP_NAME=GAME_TITLE+'.exe'
DEFAULT_THRESHOLD_IMAGE_MATCH=0.9
EXPECTED_RESOLUTION = (1280,720)

def get_game_screen(game_title, save_destination=None):
    if sys.platform in ['Windows', 'win32', 'cygwin']:

        hwnd = win32gui.FindWindow(None, game_title)

        if not hwnd:
            raise Exception(f'{game_title} not running')

        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        if x1 != EXPECTED_RESOLUTION[0] and y1 != EXPECTED_RESOLUTION[1]:
            raise Exception('Resolution not supported - supported resolution %s' %(EXPECTED_RESOLUTION))

        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        img = pyautogui.screenshot(region=(x, y, x1, y1))

        if save_destination:
            img.save(save_destination)

        return hwnd, img
    
    raise Exception('OS not supported')

def find_image_position(image_source, image_find, save_destination=None, threshold=DEFAULT_THRESHOLD_IMAGE_MATCH):
    if type(image_source) == str:
        source = np.array(Image.open(image_source).convert('RGBA'))
    else:
        source = np.array(image_source.convert('RGBA'))

    find = np.array(Image.open(image_find).convert('RGBA'))
    heat_map = cv2.matchTemplate(source, find, cv2.TM_CCOEFF_NORMED)
    max_corr = np.max(heat_map)

    if not max_corr >= threshold:
        raise Exception("Coudn't found event image")

    y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)
    # get center of image want to find, for easy click
    y += int(len(find[0]) / 2)
    x += int(len(find) / 2)

    if save_destination:
        cv2.rectangle(source, (x,y), (x+10, y+10), (255,0,0,255), 5)
        img = Image.fromarray(source, 'RGBA')
        img.save(save_destination)

    return y, x

def click_screen(y, x):
    app = pywinauto.Application().connect(path=APP_NAME)
    app[GAME_TITLE].click_input(coords=(x, y))

cur_path = 'C:\\Users\\zzxxc\\Downloads\\bit-heros'
find = '/'.join([cur_path, 'img/fishing/button.png'])
save = '/'.join([cur_path, 'img/fishing/test_get.png'])

hwnd, game_screen = get_game_screen(GAME_TITLE)
y, x = find_image_position(game_screen, find, save)
click_screen(y, x)
