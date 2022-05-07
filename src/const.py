from os import getcwd
from os.path import join

#global variables
app = None
x_multiply, y_multiply = 0, 0

GAME_TITLE='Bit Heroes'
APP_NAME=GAME_TITLE+'.exe'
DEFAULT_THRESHOLD_IMAGE_MATCH=0.7
MAX_RESOLUTION = (1600, 900)
DEBUG = True
DEBUG_SAVE_IMG = False
TITLE_BAR_HEIGHT = 8

RETRY_TIME_FIND_IMAGE = 10
SLEEP = 0.2

CUR_PATH = getcwd()
SAVE_DESTINATION = join(CUR_PATH, 'debug')

# PATH IMAGE FOLDER
FISHING_IMAGE_PATH = join(CUR_PATH, 'img', 'fishing')
COMMON_IMAGE_PATH = join(CUR_PATH, 'img', 'common')

# COMMON_IMAGE_PATH
COMMON_SMALL_X_BTN = join(COMMON_IMAGE_PATH, 'small-x.png')
COMMON_YES_BTN = join(COMMON_IMAGE_PATH, 'yes.png')
COMMON_NO_BTN = join(COMMON_IMAGE_PATH, 'no.png')
COMMON_NORMAL = join(COMMON_IMAGE_PATH, 'normal.png')
COMMON_HARD = join(COMMON_IMAGE_PATH, 'hard.png')
COMMON_HEROIC = join(COMMON_IMAGE_PATH, 'heroic.png')
COMMON_RERUN = join(COMMON_IMAGE_PATH, 'rerun.png')
COMMON_TOWN = join(COMMON_IMAGE_PATH, 'town.png')
COMMON_ACCEPT = join(COMMON_IMAGE_PATH, 'accept.png')
COMMON_AUTO_TEAM = join(COMMON_IMAGE_PATH, 'auto-team.png')
COMMON_AUTO_ON = join(COMMON_IMAGE_PATH, 'auto-on.png')
COMMON_AUTO_OFF = join(COMMON_IMAGE_PATH, 'auto-off.png')

DIFFICULTIES = {
    1: COMMON_NORMAL,
    2: COMMON_HARD,
    3: COMMON_HEROIC
}
