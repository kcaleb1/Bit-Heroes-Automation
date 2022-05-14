from farm.boss import go_boss
from farm.fishing import go_fishing
from farm.gauntlet import go_gauntlet
from farm.trials import go_trials
from farm.gvg import go_gvg
from farm.pvp import go_pvp
from farm.raid import go_raid
from farm.quest import go_quest
from farm.expedition import go_expedition
from decorator import focus_game, go_main_screen_after, terminal_wait, time_messure, check_reconnect
import warnings


@terminal_wait
@time_messure
@go_main_screen_after
@focus_game
@check_reconnect
def main():
    farms = [
        go_expedition,
        go_quest,
        go_gauntlet,
        go_gvg,
        go_pvp,
        go_raid,
        go_trials,
        go_boss  # second last, due to AFK host, or lobby not good
    ]

    # this will run each farm, to spend there energy
    empty = {}
    while len(empty) < len(farms):
        for i, farm in enumerate(farms):
            if i in empty:
                continue
            if not farm(is_loop=False):
                empty[i] = True

    go_fishing()  # this last, because no energy needed


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
