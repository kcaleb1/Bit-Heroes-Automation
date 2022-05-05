from PIL import Image
from datetime import datetime

from os import path
from utils import DEBUG_SAVE_IMG, SAVE_DESTINATION


def save_image(name: str, img: Image):
    if not DEBUG_SAVE_IMG: return
    cur = datetime.now().strftime('%y%m%d%H%M%S%f')
    img.save(path.join(SAVE_DESTINATION, f'{cur}-{name}.png'))