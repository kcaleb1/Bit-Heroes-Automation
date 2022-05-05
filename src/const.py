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
BOSS_IMAGE_PATH = join(CUR_PATH, 'img', 'boss')
RAID_IMAGE_PATH = join(CUR_PATH, 'img', 'raid')

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

# FISHING_IMAGE_PATH
FISHING_BTN = join(FISHING_IMAGE_PATH, 'button.png')
FISHING_PLAY_BTN = join(FISHING_IMAGE_PATH, 'play.png')
FISHING_START_BTN = join(FISHING_IMAGE_PATH, 'start.png')
FISHING_CAST_BTN = join(FISHING_IMAGE_PATH, 'cast.png')
FISHING_CATCH_BTN = join(FISHING_IMAGE_PATH, 'catch.png')
FISHING_TRADE_BTN = join(FISHING_IMAGE_PATH, 'trade.png')
FISHING_CLOSE_BTN = join(FISHING_IMAGE_PATH, 'close.png')
FISHING_EMPTY_BAIT = join(FISHING_IMAGE_PATH, 'empty-bait.png')
FISHING_100_PERCENT = join(FISHING_IMAGE_PATH, '100-percent.png')

# BOSS_IMAGE_PATH
BOSS_BTN = join(BOSS_IMAGE_PATH, 'button.png')

# RAID_IMAGE_PATH
RAID_BTN = join(RAID_IMAGE_PATH, 'button.png')
RAID_MOVE_RIGHT_BTN = join(RAID_IMAGE_PATH, 'move-right.png')
RAID_MOVE_LEFT_BTN = join(RAID_IMAGE_PATH, 'move-left.png')
RAID_SUMMON_BTN = join(RAID_IMAGE_PATH, 'summon.png')
RAID_BOSS_1 = join(RAID_IMAGE_PATH, 'boss-1.png')
RAID_BOSS_2 = join(RAID_IMAGE_PATH, 'boss-2.png')
RAID_BOSS_3 = join(RAID_IMAGE_PATH, 'boss-3.png')
RAID_NO_RAID = join(RAID_IMAGE_PATH, 'no-raid.png')