from mss import mss
import keyboard
import time
import cv2
import os
import numpy as np

from screen import grab
from utils.custom_mouse import mouse
from utils.misc import load_template
from logger import Logger
from win32api import GetSystemMetrics
from ui_manager import detect_screen_object, ScreenObjects



class RestartManager():

    def wait_d2_intro(self) -> bool:
        template = load_template(f"assets/templates/d2_intro_logo.png")
        template_logo = load_template(f"assets/templates/ui/main_menu/main_menu_top_left.png")
        start = time.time()
        debug_max_val = 0
        while time.time() - start < 5:
            img = grab()
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_pos = cv2.minMaxLoc(res)
            if max_val > 0.8:
                Logger.info(f"Found D2R Logo. now touch screen : [{max_pos[0]}, {max_pos[1]}]")
                mouse.move(max_pos[0] + 50, max_pos[1] + 10, randomize=10, delay_factor=[2.0, 3.0])
                time.sleep(0.5)
                mouse.click(button="left")
                time.sleep(1)
                return True

            if detect_screen_object(ScreenObjects.MainMenu).valid:
                Logger.info(f"Found Hero Selection Screen!!")
                return True
        
        mouse.move(GetSystemMetrics(0)*0.5, GetSystemMetrics(1)*0.5, randomize=8, delay_factor=[2.0, 3.0])
        mouse.click(button="left")
        return False
