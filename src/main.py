from farm.fishing import go_fishing
from farm.boss import go_boss
from farm.pvp import go_pvp
from farm.raid import go_raid
from decorator import focus_game, go_main_screen_after, terminal_wait
import warnings


@terminal_wait
@go_main_screen_after
@focus_game
def main():
    go_fishing(is_loop=True)
    go_raid(is_loop=True, boss=4, difficulty=3)
    go_boss(is_loop=True)
    go_pvp(is_loop=True, cost=5)

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
