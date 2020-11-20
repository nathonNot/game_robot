from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import pyautogui
from lib import global_data
import win32gui, win32con, win32api
from loguru import logger

# 团练授业
class TuanLian(BaseModule):

    is_act = True

    onec_button = []
    chick_button = None

    def __init__(self):
        logger.info("初始化团练授业模块")

    # def fram_update(self):
    #     if len(global_data.hwnd_list) <= 0:
    #         return
    #     for hwnd in global_data.hwnd_list:
    #         self.update_hwnd(hwnd)

    def update_hwnd(self, hwnd):
        # 获取窗口左上角和右下角坐标
        self.onec_button.clear()
        up = Controls.localall("image\\tl_up.png", hwnd)
        down = Controls.localall("image\\tl_down1.png", hwnd)
        right = Controls.localall("image\\tl_right1.png", hwnd)
        left = Controls.localall("image\\tl_left.bmp", hwnd)
        tl_k = Controls.localall("image\\tl_k.png", hwnd)
        tl_j = Controls.localall("image\\tl_j.png", hwnd)
        if up:
            self.add_button_cilck(up, "up", win32con.VK_UP)
        if down:
            self.add_button_cilck(down, "down", win32con.VK_DOWN)
        if right:
            self.add_button_cilck(right, "right", win32con.VK_RIGHT)
        if left:
            self.add_button_cilck(left, "left", win32con.VK_LEFT)
        if tl_k:
            self.add_button_cilck(tl_k, "k", 0x4B)
        if tl_j:
            self.add_button_cilck(tl_j, "j", 0x4A)
        last_x = 0
        if len(self.onec_button) > 0:
            pyautogui.FAILSAFE = False
            self.de_repetition()
            logger.info(self.onec_button)
            # pyautogui.leftClick(self.chick_button)
            # win32api.SendMessage(hwnd, win32con.WM_ACTIVATE,0x2,0)
            # win32api.SendMessage(hwnd, win32con.WM_IME_SETCONTEXT,0x1,0xC000000F)
            # win32api.SendMessage(hwnd, win32con.WM_IME_NOTIFY,0x2,0)
            Controls.activate_hwnd(hwnd)
            for key in self.onec_button:
                if (key[1] - last_x) <= 5:
                    continue
                Controls.key_post(hwnd, key[2])
                last_x = key[1]
                # pyautogui.press(key[0])
            # pyautogui.moveTo(0, 0)

    def add_button_cilck(self, button_find, button_name, vk_key):
        for button in button_find:
            if button is None:
                continue
            new_list = [button_name, button.left, vk_key]
            if new_list in self.onec_button:
                continue
            self.onec_button.append(new_list)
            self.chick_button = button

    def de_repetition(self):
        self.onec_button.sort(key=lambda x: x[1])
        new_list = []
        for button in self.onec_button:
            if button in new_list:
                continue
            new_button = [button[0], button[1] - 1, button[2]]
            if new_button in new_list:
                continue
            new_list.append(button)
        self.onec_button = new_list