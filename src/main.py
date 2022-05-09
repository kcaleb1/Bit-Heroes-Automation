from farm.boss import go_boss
from farm.fishing import go_fishing
from farm.gauntlet import go_gauntlet
from farm.gvg import go_gvg
from farm.pvp import go_pvp
from farm.raid import go_raid
from decorator import focus_game, go_main_screen_after, terminal_wait, time_messure
import warnings


@terminal_wait
@time_messure
@go_main_screen_after
@focus_game
def main():
    go_gauntlet()
    go_gvg()
    go_pvp()
    go_raid()

    go_boss() # second last, due to AFK host, or lobby not good
    go_fishing() # this last, because no energy needed

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
