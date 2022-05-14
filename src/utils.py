from window import click_screen_and_sleep, get_game_screen, press_escape
from debug import save_image_dbg, save_print_dbg
from error import *
from const import *
import const
from time import sleep
import os
import cv2
import numpy as np
from PIL import Image, ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


def find_image_position(image_source: Image, image_find_path: str, threshold=None):
    image_path = image_find_path.replace(IMG_PATH+os.sep, '')
    name = '_'.join(image_path.split(os.sep))

    if type(image_source) == str:
        source = np.array(Image.open(image_source).convert('RGBA'))
    else:
        source = np.array(image_source.convert('RGBA'))

    # convert from maximum size to current game resolution
    find_image = Image.open(image_find_path).convert('RGBA')
    old_width, old_height = find_image._size
    new_height = int(old_height * const.y_multiply)
    new_width = int(old_width * const.x_multiply)
    if old_width != new_width or old_height != new_height:
        find_image = find_image.resize(
            (new_width, new_height), Image.ANTIALIAS)
        old_width, old_height = find_image._size
        # save_image_dbg(f'resize-{name}', find_image)
    find = np.array(find_image)

    heat_map = cv2.matchTemplate(source, find, cv2.TM_CCOEFF_NORMED)
    max_corr = round(np.max(heat_map), 2)
    # threshold = min(round((const.y_multiply + const.y_multiply) / 2, 2), DEFAULT_THRESHOLD_IMAGE_MATCH)

    save_print_dbg(f'matching: {max_corr:.2f}/{threshold}')
    # save_print_dbg(f'resize: y:{const.y_multiply:.2f} x:{const.x_multiply:.2f}\tmatching: {max_corr:.2f}/{threshold}')

    if threshold and not max_corr >= threshold:
        raise ImageNotFoundException(image_path=image_path)

    y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)

    y += int(old_height / 2)
    x += int(old_width / 2)

    cv2.rectangle(source, (x, y), (x+5, y+5), (255, 0, 0, 255), 5)
    img = Image.fromarray(source, 'RGBA')
    save_image_dbg(f'find_image_position-{name}', img)

    return y, x


def find_image_and_click_then_sleep(
    path: str,
    retry_time=RETRY_TIME_FIND_IMAGE,
    sleep_duration=SLEEP,
    threshold=DEFAULT_THRESHOLD_IMAGE_MATCH,
    find_interval=SLEEP,
    ignore_exception=False,
):
    y, x = 0, 0
    try:
        y, x = find_image(path, retry_time, threshold,
                          find_interval=find_interval)
    except Exception as ex:
        if ignore_exception:
            return
        raise ex
    click_screen_and_sleep(y, x, sleep_duration)


def find_image(
    path: str,
    retry_time=RETRY_TIME_FIND_IMAGE,
    threshold=DEFAULT_THRESHOLD_IMAGE_MATCH,
    find_interval=SLEEP,
    game_screen=None,
    return_game_screen=False,
):
    y, x = -1, -1
    e = None
    for i in range(retry_time):
        save_print_dbg(f"retry: {i} on {path.replace(IMG_PATH, '')}", end='\t')
        if game_screen == None:
            cur_game_screen = get_game_screen()
        else:
            cur_game_screen = game_screen
        try:
            y, x = find_image_position(cur_game_screen, path, threshold)
            if return_game_screen:
                return y, x, cur_game_screen
            return y, x
        except Exception as ex:
            e = ex
        sleep(find_interval)
    raise e


def go_main_screen():
    old_dbg_name = const.dbg_name.__str__()
    const.dbg_name = 'escape'
    save_print_dbg("**Debug for action 'press escape'")
    while True:
        press_escape()
        sleep(0.5)
        try:
            find_image(COMMON_NO, retry_time=1)
            sleep(0.5)
            press_escape()
            break
        except:
            pass
    save_print_dbg("**Finished action 'press escape'")
    const.dbg_name = old_dbg_name


def run_or_raise_exception(fun, exception: Exception):
    try:
        fun()
        raise exception()
    except exception as ex:
        raise ex
    except KeyboardInterrupt as ex:
        raise ex
    except:
        pass


def enable_auto_on() -> bool:
    try:
        find_image(COMMON_AUTO_ON, retry_time=1, threshold=0.9)
        return True
    except:
        pass

    try:
        find_image_and_click_then_sleep(
            COMMON_AUTO_OFF, retry_time=1, threshold=0.9)
        return True
    except:
        pass

    return False


def click_town() -> bool:
    try:
        y, x = find_image(COMMON_TOWN, retry_time=1, threshold=0.9)
        sleep(1)
        click_screen_and_sleep(y, x)
        return True
    except:
        return False


def check_no_energy():
    run_or_raise_exception(
        lambda: find_image_and_click_then_sleep(
            COMMON_NO, threshold=0.9, retry_time=3),
        NoEnergyException
    )


def click_cost_and_play(cost, menu_cost=COMMON_COST, play_btn=COMMON_PLAY):
    find_image_and_click_then_sleep(menu_cost, retry_time=5)

    try:
        find_image_and_click_then_sleep(
            cost, retry_time=5, sleep_duration=0.5, threshold=0.9)
        find_image(cost, retry_time=5)
        press_escape()
    except:
        press_escape()
    finally:
        sleep(SLEEP)

    find_image_and_click_then_sleep(play_btn, retry_time=5, sleep_duration=1)
    check_no_energy()


def fight_wait_town():
    while not enable_auto_on():
        sleep(SLEEP)
    while not click_town():
        sleep(1)


def decline_except_persure(decline):
    y, x, img = None, None, None
    try:
        y, x, img = find_image(decline, retry_time=1, return_game_screen=True)
        find_image(COMMON_PERSUADE, retry_time=1, game_screen=img)
    except:
        if y != None:
            click_screen_and_sleep(y, x, sleep_duration=0.5)
            find_image_and_click_then_sleep(
                COMMON_YES, retry_time=1, ignore_exception=True)
