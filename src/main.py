import warnings
import multiprocessing
from farm.boss import Boss
from farm.fishing import Fishing
from farm.gauntlet import Gauntlet
from farm.invasion import Invasion
from farm.trials import Trails
from farm.gvg import Gvg
from farm.pvp import Pvp
from farm.raid import Raid
from farm.quest import Quest
from farm.expedition import Expedition
from decorator import create_usage_file
from ui.main_screen import MainScreen


@create_usage_file
def main_v2():
    farms = [
        Raid,
        Quest,
        Expedition,
        Gauntlet,
        Gvg,
        Invasion,
        Pvp,
        Trails,
        Boss,  # second last, due to AFK host, or lobby not good
        Fishing
    ]
    MainScreen(farms).display()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main_v2()
