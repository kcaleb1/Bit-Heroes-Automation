from os import getcwd
from os.path import join, isdir
from json import load

#global variables
app = None
hwnd = None
app_pos = (0, 0, 0, 0)
x_multiply, y_multiply = 1, 1
dbg_name = 'initialize'
cfg = {}

### --------------------------------------------
CUR_PATH = getcwd()
DEBUG_PATH = getcwd()

CONFIG_FILE = join(CUR_PATH, 'config.json')
with open(CONFIG_FILE, 'r') as f:
    cfg = load(f)

IMG_PATH = join(CUR_PATH, 'img')
SAVE_DEBUG_PATH = join(DEBUG_PATH, 'debug')
DEBUG_TEXT_PATH = join(SAVE_DEBUG_PATH, 'debug.log')
SAVE_ESCAPE_IMG_PATH = join(SAVE_DEBUG_PATH, 'escape')

COMMON_IMAGE_PATH = join(IMG_PATH, 'common')
# COMMON_IMAGE_PATH
COMMON_ACCEPT = join(COMMON_IMAGE_PATH, 'accept.png')
COMMON_AUTO_OFF = join(COMMON_IMAGE_PATH, 'auto-off.png')
COMMON_AUTO_ON = join(COMMON_IMAGE_PATH, 'auto-on.png')
COMMON_AUTO_TEAM = join(COMMON_IMAGE_PATH, 'auto-team.png')
COMMON_CLOSE = join(COMMON_IMAGE_PATH, 'close.png')
COMMON_COST = join(COMMON_IMAGE_PATH, 'cost.png')
COMMON_DECLINE = join(COMMON_IMAGE_PATH, 'decline.png')
COMMON_FIGHT = join(COMMON_IMAGE_PATH, 'fight.png')
COMMON_NO = join(COMMON_IMAGE_PATH, 'no.png')
COMMON_PLAY = join(COMMON_IMAGE_PATH, 'play.png')
COMMON_RERUN = join(COMMON_IMAGE_PATH, 'rerun.png')
COMMON_SMALL_X = join(COMMON_IMAGE_PATH, 'small-x.png')
COMMON_TOWN = join(COMMON_IMAGE_PATH, 'town.png')
COMMON_YES = join(COMMON_IMAGE_PATH, 'yes.png')

COSTS = {
    1: join(COMMON_IMAGE_PATH, 'cost-1.png'),
    2: join(COMMON_IMAGE_PATH, 'cost-2.png'),
    3: join(COMMON_IMAGE_PATH, 'cost-3.png'),
    4: join(COMMON_IMAGE_PATH, 'cost-4.png'),
    5: join(COMMON_IMAGE_PATH, 'cost-5.png')
}

DIFFICULTIES = {
    1: join(COMMON_IMAGE_PATH, 'normal.png'),
    2: join(COMMON_IMAGE_PATH, 'hard.png'),
    3: join(COMMON_IMAGE_PATH, 'heroic.png')
}

GAME_TITLE = 'Bit Heroes'
APP_NAME = GAME_TITLE+'.exe'
DEFAULT_THRESHOLD_IMAGE_MATCH = 0.75
MAX_RESOLUTION = (800, 480)
TITLE_BAR_HEIGHT = 10
PREFIX_CLICK = 10

TIME_FORMAT = '%y%m%d%H%M%S%f'

RETRY_TIME_FIND_IMAGE = 10

SLEEP = cfg.get('capture_interval')
DEBUG = cfg.get('debug', False)
DEBUG_SAVE_IMG = cfg.get('save_captured_image', False)
