import keyboard
from logger import Logger
import cv2
import time
import numpy as np
from utils.misc import cut_roi, color_filter, wait
from utils.custom_mouse import mouse
from screen import grab, convert_screen_to_monitor
from config import Config
from template_finder import TemplateFinder
from ui_manager import wait_until_visible, ScreenObjects

def is_left_skill_selected(template_list: list[str]) -> bool:
    """
    :return: Bool if skill is currently the selected skill on the left skill slot.
    """
    skill_left_ui_roi = Config().ui_roi["skill_left"]
    for template in template_list:
        if TemplateFinder().search(template, grab(), threshold=0.84, roi=skill_left_ui_roi).valid:
            return True
    return False

def has_tps() -> bool:
    """
    :return: Returns True if botty has town portals available. False otherwise
    """
    if Config().char["tp"]:
        keyboard.send(Config().char["tp"])
        if not (tps_remain := wait_until_visible(ScreenObjects.TownPortalSkill, timeout=4).valid):
            Logger.warning("You are out of tps")
            if Config().general["info_screenshots"]:
                cv2.imwrite("./info_screenshots/debug_out_of_tps_" + time.strftime("%Y%m%d_%H%M%S") + ".png", grab())
        return tps_remain
    else:
        return False

def select_tp(tp_hotkey):
    if tp_hotkey and not is_right_skill_selected(
        ["TELE_ACTIVE", "TELE_INACTIVE"]):
        keyboard.send(tp_hotkey)
        wait(0.1, 0.2)
    return is_right_skill_selected(["TELE_ACTIVE", "TELE_INACTIVE"])

def is_right_skill_active() -> bool:
    """
    :return: Bool if skill is red/available or not. Skill must be selected on right skill slot when calling the function.
    """
    roi = [
        Config().ui_pos["skill_right_x"] - (Config().ui_pos["skill_width"] // 2),
        Config().ui_pos["skill_y"] - (Config().ui_pos["skill_height"] // 2),
        Config().ui_pos["skill_width"],
        Config().ui_pos["skill_height"]
    ]
    img = cut_roi(grab(), roi)
    avg = np.average(img)
    return avg > 75.0

def is_right_skill_selected(template_list: list[str]) -> bool:
    """
    :return: Bool if skill is currently the selected skill on the right skill slot.
    """
    skill_right_ui_roi = Config().ui_roi["skill_right"]
    for template in template_list:
        if TemplateFinder().search(template, grab(), threshold=0.84, roi=skill_right_ui_roi).valid:
            return True
    return False

def get_skill_charges(ocr, img: np.ndarray = None):
    if img is None:
        img = grab()
    x, y, w, h = Config().ui_roi["skill_right"]
    x = x - 1
    y = y + round(h/2)
    h = round(h/2 + 5)
    img = cut_roi(img, [x, y, w, h])
    mask, _ = color_filter(img, Config().colors["skill_charges"])
    ocr_result = ocr.image_to_text(
        images = mask,
        model = "engd2r_inv_th",
        psm = 7,
        word_list = "",
        scale = 1.4,
        crop_pad = False,
        erode = False,
        invert = True,
        threshold = 0,
        digits_only = True,
        fix_regexps = False,
        check_known_errors = False,
        check_wordlist = False,
        word_match_threshold = 0.5
    )[0]
    try:
        return int(ocr_result.text)
    except:
        return None

def teleport_key_bind(teleport_key):
        if select_tp(teleport_key):
            return
        keyboard.send(Config().char["skill_speed_bar"])
        wait(0.4, 0.45)
        tele_img = TemplateFinder().search("TELE_INACTIVE", grab())
        if tele_img.valid:
            x, y = convert_screen_to_monitor(tele_img.center)            
            Logger.debug(f"Found Teleport skill icon.")
            mouse.move(x, y, randomize=[5, 5], delay_factor=[1.0, 1.8])
            wait(0.2, 0.3)
            keyboard.send(teleport_key)
            wait(0.2, 0.3)
        
        keyboard.send(Config().char["skill_speed_bar"])
        wait(0.2, 0.3)
