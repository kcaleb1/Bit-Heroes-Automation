from farm import Farm
from utils import check_no_energy, click_town_or_rerun, enable_auto_on, find_image, find_image_and_click_then_sleep, raise_exception_when_runnable, sleep
from window import press_escape
from const import *
from error import *
from datetime import datetime


FEATURE_PATH = join(IMG_PATH, 'boss')
BTN = join(FEATURE_PATH, 'button.png')
FULL_TXT = join(FEATURE_PATH, 'full.png')
JOIN_BTN = join(FEATURE_PATH, 'join.png')
READY_BTN = join(FEATURE_PATH, 'ready.png')
START_BTN = join(FEATURE_PATH, 'start.png')
SUMMON_BTN = join(FEATURE_PATH, 'summon.png')
SUMMON_BOSS_BTN = join(FEATURE_PATH, 'summon-boss.png')
SUMMON_3_BTN = join(FEATURE_PATH, 'summon-3.png')
LEFT_BTN = join(FEATURE_PATH, 'left.png')
TIER_OPTION = join(FEATURE_PATH, 'tier-option.png')
DIFFICULTY_OPTION = join(FEATURE_PATH, 'difficulty-option.png')
INVITE_BTN = join(FEATURE_PATH, 'invite.png')

BOSSES = {
    "Orlag Clan": join(FEATURE_PATH, 'orlag-clan.png'),
    "Netherworld": join(FEATURE_PATH, 'netherworld.png')
}

BOSS_DIFFICULTIES = {
    "Normal": join(FEATURE_PATH, 'normal.png'),
    "Hard": join(FEATURE_PATH, 'hard.png'),
    "Heroic": join(FEATURE_PATH, 'heroic.png'),
}


class Boss(Farm):
    feature = 'boss'
    bosses = list(BOSSES.keys())

    def __init__(self):
        super().__init__()
        # boss will not use rerun mode due to it such for this mode
        self.rerun_mode = False
        self.brush_force_energy = False
        self.button = BTN

    def config_run(self):
        # boss will not use rerun mode due to it such for this mode
        self.rerun_mode = False
        self.brush_force_energy = False
        # self.select_run_summon_boss()
        self.select_run_join_lobby()

    def select_run_summon_boss(self):
        find_image_and_click_then_sleep(SUMMON_BTN)

        for _ in range(10):
            try:
                find_image(BOSSES[self.boss], retry_time=3)
                break
            except:
                find_image_and_click_then_sleep(LEFT_BTN)
        else:
            raise UnableJoinException("???")

        find_image_and_click_then_sleep(SUMMON_BOSS_BTN)

        # TODO Tier selectable
        # find_image_and_click_then_sleep(TIER_OPTION)

        # TODO Cost selectable
        # click_cost_and_play(cost=BOSS_DIFFICULTIES[self.difficulty],
        #                     menu_cost=DIFFICULTY_OPTION,
        #                     play_btn=SUMMON_3_BTN)
        find_image_and_click_then_sleep(SUMMON_3_BTN)
        check_no_energy()

        # wait for full lobby
        while True:
            try:
                find_image_and_click_then_sleep(INVITE_BTN, retry_time=1)
            except:
                break

        # then start
        while True:
            clicked = False
            try:
                find_image_and_click_then_sleep(START_BTN, retry_time=1)
                clicked = True
                find_image(START_BTN)
            except:
                if clicked:
                    break

        while not enable_auto_on():
            sleep(SLEEP)

        while not click_town_or_rerun():
            sleep(SLEEP)

    def is_host(self) -> bool:
        # check when become host, leave lobby and rerun
        try:
            find_image(START_BTN, retry_time=1)
            press_escape()
            return True
        except:
            return False

    def check_close(self):
        raise_exception_when_runnable(
            lambda: find_image(COMMON_CLOSE, retry_time=1),
            UnableJoinException
        )

    def select_run_join_lobby(self):
        try:
            find_image_and_click_then_sleep(
                JOIN_BTN, retry_time=5, sleep_duration=1)
        except:
            raise UnableJoinException()

        check_no_energy()
        for _ in range(10):
            try:
                find_image_and_click_then_sleep(READY_BTN, retry_time=1)
                break
            except:
                pass

            self.check_close()

            if self.is_host():
                find_image_and_click_then_sleep(COMMON_YES)
                raise UnableJoinException()
        else:
            raise UnableJoinException()

        start_time = datetime.now()
        is_started = False
        is_auto_on = False
        is_pressed_escape = False
        while True:
            is_started = click_town_or_rerun()
            if is_started:
                break

            if not is_auto_on:
                # check got kicked from room
                self.check_close()

                if self.is_host():
                    break

                # this will help to exit the lobby when host afk to long
                # press escape, in case of already in-game, this will turn off auto play
                # and the click COMMON_AUTO_OFF will handle it
                if (datetime.now() - start_time).seconds >= 60:
                    if is_pressed_escape:
                        is_auto_on = enable_auto_on()
                        if is_auto_on:
                            continue
                        break
                    press_escape()
                    is_pressed_escape = True

                is_auto_on = enable_auto_on()

        if not is_started:
            sleep(SLEEP)
            find_image_and_click_then_sleep(COMMON_YES)
            raise UnableJoinException()

    def get_config(self):
        super().get_config()
        self.cost = self.cfg.get('cost', 1)
        self.is_summon = self.cfg.get('is_summon', False)
        self.is_solo = self.cfg.get('is_solo', False)
        self.boss = self.cfg.get('boss', self.bosses[0])
        self.tier = self.cfg.get('tier', )
        self.difficulty = self.cfg.get('difficulty', 1)
