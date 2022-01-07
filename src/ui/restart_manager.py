from mss import mss
import keyboard
import time
import cv2
import os
import numpy as np

from utils.custom_mouse import mouse
from utils.misc import load_template
from logger import Logger
from template_finder import TemplateFinder
from win32api import GetSystemMetrics



class RestartManager():

    def __init__(self, monitor: int = 0):
        self._sct = mss()        
        monitor_idx = monitor + 1 # sct saves the whole screen (including both monitors if available at index 0, then monitor 1 at 1 and 2 at 2)
        if len(self._sct.monitors) == 1:
            Logger.error("How do you not have a monitor connected?!")
            os._exit(1)
        if monitor_idx >= len(self._sct.monitors):
            Logger.warning("Monitor index not available! Choose a smaller number for 'monitor' in the param.ini. Forcing value to 0 for now.")
            monitor_idx = 1
        self._monitor_roi = self._sct.monitors[monitor_idx]

    def grab(self) -> np.ndarray:
        img = np.array(self._sct.grab(self._monitor_roi))
        return img[:, :, :3]
        
    def wait_d2_intro(self) -> bool:
        template = load_template(f"assets/templates/d2_intro_logo.png", 1.0)
        template_logo = load_template(f"assets/templates/main_menu_top_left.png", 1.0)
        start = time.time()
        debug_max_val = 0
        while time.time() - start < 5:
            img = self.grab()
            self._sct = mss()
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            res2 = cv2.matchTemplate(img, template_logo, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_pos = cv2.minMaxLoc(res)
            _, max_val2, _, max_pos2 = cv2.minMaxLoc(res2)
            if max_val > 0.8:
                Logger.info(f"Found D2R Logo. now touch screen")
                mouse.move(max_pos[0] + 50, max_pos[1] + 10, randomize=10, delay_factor=[2.0, 3.0])
                mouse.click(button="left")
                time.sleep(1)
                return True;
            elif max_val2 > 0.8:
                Logger.info(f"Found Hero Selection Screen!!")
                return True;
        
        mouse.move(GetSystemMetrics(0)*0.5, GetSystemMetrics(1)*0.5, randomize=8, delay_factor=[2.0, 3.0])
        mouse.click(button="left")
        return False;
