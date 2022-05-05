import cv2
import numpy as np
from PIL import Image, ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

import os
from time import sleep
from const import *
from error import *
from debug import save_image
from window import click_screen_and_sleep, get_game_screen, get_app, press_escape


def find_image_position(image_source, image_find_path: str, threshold=None):
    if type(image_source) == str:
        source = np.array(Image.open(image_source).convert('RGBA'))
    else:
        source = np.array(image_source.convert('RGBA'))

    # convert from maximum size to current game resolution
    find_image = Image.open(image_find_path).convert('RGBA')
    old_width, old_height = find_image._size
    if x_multiply != 0 and y_multiply != 0:
        new_height = int(old_height * x_multiply)
        new_width = int(old_width * y_multiply)
        find_image = find_image.resize((new_width, new_height), Image.ANTIALIAS)
        old_width, old_height = find_image._size
    find = np.array(find_image)

    heat_map = cv2.matchTemplate(source, find, cv2.TM_CCOEFF_NORMED)
    max_corr = np.max(heat_map)

    print(max_corr, threshold)
    if threshold and not max_corr >= threshold:
        raise ImageNotFoundException("Could not found event image")

    y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)

    y += int(old_height / 2)
    x += int(old_width / 2)

    if DEBUG:
        cv2.rectangle(source, (x,y), (x+5, y+5), (255,0,0,255), 5)
        img = Image.fromarray(source, 'RGBA')
        feature, file_name = image_find_path.split(os.sep)[-2:]
        name = '_'.join(file_name.split('.')[0].split('-'))
        save_image(f'find_image_position-{feature}-{name}', img)

    return y, x


def find_image_and_click_then_sleep(path, retry_time=RETRY_TIME_FIND_IMAGE, sleep_duration=SLEEP, threshold=DEFAULT_THRESHOLD_IMAGE_MATCH):
    y, x = find_image(path, retry_time, threshold)
    click_screen_and_sleep(y, x, sleep_duration)


def find_image(path, retry_time=RETRY_TIME_FIND_IMAGE, threshold=DEFAULT_THRESHOLD_IMAGE_MATCH):
    y, x = -1 , -1
    e = None
    for i in range(retry_time):
        print(i, path)
        game_screen = get_game_screen()
        try:
            y, x = find_image_position(game_screen, path, threshold)
            return y, x
        except Exception as ex:
            e = ex
        sleep(SLEEP)
        
    raise e


def go_main_screen():
    while True:
        press_escape()
        sleep(SLEEP)
        try:
            find_image_and_click_then_sleep(COMMON_NO_BTN, retry_time=3)
            return
        except:
            pass