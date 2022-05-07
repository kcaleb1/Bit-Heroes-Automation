from farm.fishing import go_fishing
from farm.boss import go_boss
from farm.pvp import go_pvp
from farm.raid import go_raid
from utils import go_main_screen
import warnings


def main():
    go_fishing(is_loop=True)
    go_raid(is_loop=True, boss=4, difficulty=3)
    go_boss(is_loop=True)
    go_pvp(is_loop=True, cost=5)

    go_main_screen()

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
