from genericpath import isdir
import traceback
from PIL import Image
from datetime import datetime
from os import path, mkdir
from const import DEBUG_SAVE_IMG, SAVE_DEBUG_PATH, DEBUG, DEBUG_TEXT_PATH, TIME_FORMAT
import const


def save_image_dbg(name: str, img: Image):
    if not DEBUG_SAVE_IMG:
        return
    if not isdir(SAVE_DEBUG_PATH):
        mkdir(SAVE_DEBUG_PATH)
    folder_path = path.join(SAVE_DEBUG_PATH, const.dbg_name)
    if not path.isdir(folder_path):
        mkdir(folder_path)
    cur = datetime.now().strftime(TIME_FORMAT)
    img.save(path.join(folder_path, f'{cur}-{name}.png'))


def save_print_dbg(txt: str, end='\n', is_print=True):
    if not DEBUG:
        return
    print(txt, end=end)
    if not isdir(SAVE_DEBUG_PATH):
        mkdir(SAVE_DEBUG_PATH)
    with open(DEBUG_TEXT_PATH, 'a+') as f:
        f.write(str(txt) + end)


def print_stacktrace():
    print(traceback.format_exc())
