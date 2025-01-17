from char import IChar
from config import Config
from logger import Logger
from pather import Location, Pather
from typing import Union
from item.pickit import PickIt
import template_finder
from town.town_manager import TownManager
from utils.misc import wait
from ui import loading
from game_stats import GameStats

class Pindle:
    def __init__(
        self,
        pather: Pather,
        town_manager: TownManager,
        char: IChar,
        pickit: PickIt,
        game_stats: GameStats = None
    ):
        self._pather = pather
        self._town_manager = town_manager
        self._char = char
        self._pickit = pickit
        self._game_stats = game_stats

    def approach(self, start_loc: Location) -> Union[bool, Location]:
        # Go through Red Portal in A5
        Logger.info("Run Pindle")
        loc = self._town_manager.go_to_act(5, start_loc)
        if not loc:
            return False
        if not self._pather.traverse_nodes((loc, Location.A5_NIHLATHAK_PORTAL), self._char):
            return False
        wait(0.5, 0.6)
        found_loading_screen_func = lambda: loading.wait_for_loading_screen(2.0)
        if not self._char.select_by_template("A5_RED_PORTAL", found_loading_screen_func, telekinesis=False):
            return False
        return Location.A5_PINDLE_START

    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        # Kill Pindle
        if not template_finder.search_and_wait(["PINDLE_0", "PINDLE_1"], threshold=0.65, timeout=20).valid:
            return False
        if do_pre_buff:
            self._char.pre_buff()
        # move to pindle
        if self._char.capabilities.can_teleport_natively or ( self._char.capabilities.can_teleport_with_charges and Config().char["teleport_type"] == 0 ):
            self._pather.traverse_nodes_fixed("pindle_safe_dist", self._char, use_tp_charge=True)
        else:
            if not self._pather.traverse_nodes((Location.A5_PINDLE_START, Location.A5_PINDLE_SAFE_DIST), self._char):
                return False
        self._char.kill_pindle()
        wait(0.2, 0.3)
        picked_up_items = self._pickit.pick_up_items(self._char)
        self._game_stats.log_kill_pindle()
        return (Location.A5_PINDLE_END, picked_up_items)
