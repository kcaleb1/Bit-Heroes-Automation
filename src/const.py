from os import getcwd
from os.path import join
from json import load

# global variables
app = None
dbg_name = 'initialize'
cfg = {}

# --------------------------------------------
CUR_PATH = getcwd()

USAGE_FILE = join(CUR_PATH, 'usage.json')
CONFIG_FILE = join(CUR_PATH, 'config.json')
with open(CONFIG_FILE, 'r') as f:
    cfg = load(f)

IMG_PATH = join(CUR_PATH, 'img')
SAVE_DEBUG_PATH = join(CUR_PATH, 'debug')
DEBUG_TEXT_PATH = join(SAVE_DEBUG_PATH, 'debug.log')
SAVE_ESCAPE_IMG_PATH = join(SAVE_DEBUG_PATH, 'escape')

COMMON_IMAGE_PATH = join(IMG_PATH, 'common')
UI_IMAGE_PATH = join(IMG_PATH, 'ui')

# COMMON_IMAGE_PATH
COMMON_ACCEPT = join(COMMON_IMAGE_PATH, 'accept.png')
COMMON_AUTO_OFF = join(COMMON_IMAGE_PATH, 'auto-off.png')
COMMON_AUTO_ON = join(COMMON_IMAGE_PATH, 'auto-on.png')
COMMON_AUTO_TEAM = join(COMMON_IMAGE_PATH, 'auto-team.png')
COMMON_CLOSE = join(COMMON_IMAGE_PATH, 'close.png')
COMMON_COST = join(COMMON_IMAGE_PATH, 'cost.png')
COMMON_FIGHT = join(COMMON_IMAGE_PATH, 'fight.png')
COMMON_NO = join(COMMON_IMAGE_PATH, 'no.png')
COMMON_PLAY = join(COMMON_IMAGE_PATH, 'play.png')
COMMON_RERUN = join(COMMON_IMAGE_PATH, 'rerun.png')
COMMON_SMALL_X = join(COMMON_IMAGE_PATH, 'small-x.png')
COMMON_TOWN = join(COMMON_IMAGE_PATH, 'town.png')
COMMON_YES = join(COMMON_IMAGE_PATH, 'yes.png')
COMMON_PERSUADE = join(COMMON_IMAGE_PATH, 'persuade.png')
COMMON_SPECIAL_COST = join(COMMON_IMAGE_PATH, 'special-cost.png')
COMMON_RECONNECT = join(COMMON_IMAGE_PATH, 'reconnect.png')
COMMON_OPEN = join(COMMON_IMAGE_PATH, 'open.png')
COMMON_TREASURE_KEY = join(COMMON_IMAGE_PATH, 'treasure-key.png')
COMMON_NOT_ENOUGH = join(COMMON_IMAGE_PATH, 'not-enough.png')
COMMON_NO_ENERGY_BAR_1 = join(COMMON_IMAGE_PATH, 'no-energy-bar-1.png')
COMMON_NO_ENERGY_BAR_2 = join(COMMON_IMAGE_PATH, 'no-energy-bar-2.png')
COMMON_DECLINE_TREASURE = join(COMMON_IMAGE_PATH, 'decline-treasure.png')
COMMON_TEAM_NOT_FULL = join(COMMON_IMAGE_PATH, 'team-not-full.png')

COSTS = {
    1: join(COMMON_IMAGE_PATH, 'cost-1.png'),
    2: join(COMMON_IMAGE_PATH, 'cost-2.png'),
    3: join(COMMON_IMAGE_PATH, 'cost-3.png'),
    4: join(COMMON_IMAGE_PATH, 'cost-4.png'),
    5: join(COMMON_IMAGE_PATH, 'cost-5.png')
}

LIST_COSTS = list(COSTS.keys())

DIFFICULTIES = {
    'Normal': join(COMMON_IMAGE_PATH, 'normal.png'),
    'Hard': join(COMMON_IMAGE_PATH, 'hard.png'),
    'Heroic': join(COMMON_IMAGE_PATH, 'heroic.png')
}

LIST_DIFFICULTIES = list(DIFFICULTIES.keys())

STEAM_ID = 666860
GAME_TITLE = 'Bit Heroes'
APP_NAME = GAME_TITLE+'.exe'
DEFAULT_THRESHOLD_IMAGE_MATCH = 0.8
MAX_RESOLUTION = (800, 480)
TITLE_BAR_HEIGHT = 10
PREFIX_CLICK = 10

TIME_FORMAT = '%y%m%d%H%M%S'
READABLE_TIME_FORMAT = '%y/%m/%d %H:%M:%S'

RETRY_TIME_FIND_IMAGE = 10

SLEEP = cfg.get('capture_interval', 0.3)
DEBUG = cfg.get('debug', False)
DEBUG_SAVE_IMG = cfg.get('save_captured_image', False)

SECOND = 1
MINUTE = 60 * SECOND
FIVE_MINUTE = 5 * MINUTE
TRIGGER_RECONNECT_CHECK = 10 * MINUTE

SECOND_MS = 1000
