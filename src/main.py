from faulthandler import is_enabled
from farm.fishing import go_fishing
from farm.boss import go_boss
from farm.raid import go_raid
from utils import go_main_screen


go_fishing(is_loop=True)
# go_boss(is_loop=False)
go_raid(is_loop=False)
