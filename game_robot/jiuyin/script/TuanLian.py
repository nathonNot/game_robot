from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import pyautogui
from lib import global_data
import win32gui


# 团练授业
class TuanLian(BaseModule):

    is_act = True

    onec_button = []
    chick_button = None

    def __init__(self):
        print("初始化团练授业模块")

    def fram_update(self):
        if len(global_data.hwnd_list) <= 0:
            return
        for hwnd in global_data.hwnd_list:
            self.update_hwnd(hwnd)

    def update_hwnd(self, hwnd):
        # 获取窗口左上角和右下角坐标
        xleft, ytop, xright, ybottom = win32gui.GetWindowRect(hwnd)
        form = (xleft, ytop, (xright - xleft), (ybottom - ytop))
        self.onec_button.clear()
        up = Controls.get_screen_box_all("image\\tl_up.png", region=form)
        down = Controls.get_screen_box_all("image\\tl_down.png", region=form)
        right = Controls.get_screen_box_all("image\\tl_right.png", region=form)
        left = Controls.get_screen_box_all("image\\tl_left.png", region=form)
        tl_k = Controls.get_screen_box_all("image\\tl_k.png", region=form)
        tl_j = Controls.get_screen_box_all("image\\tl_j.png", region=form)
        if up:
            self.add_button_cilck(up, "up")
        if down:
            self.add_button_cilck(down, "down")
        if right:
            self.add_button_cilck(right, "right")
        if left:
            self.add_button_cilck(left, "left")
        if tl_k:
            self.add_button_cilck(tl_k, "k")
        if tl_j:
            self.add_button_cilck(tl_j, "j")
        last_x = 0
        if len(self.onec_button) > 0:
            pyautogui.FAILSAFE = False
            self.onec_button.sort(key=lambda x: x[1])
            print(self.onec_button)
            pyautogui.leftClick(self.chick_button)
            for key in self.onec_button:
                if (key[1] - last_x) <= 5:
                    continue
                last_x = key[1]
                pyautogui.press(key[0])
            pyautogui.moveTo(0, 0)

    def add_button_cilck(self, button_find, button_name):
        for button in button_find:
            self.onec_button.append([button_name, button.left])
            self.chick_button = button
