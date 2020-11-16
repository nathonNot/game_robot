from lib.BaseModule import BaseModule
import lib.gui_controls as controls
import pyautogui


# 手机刺探
class CiTan(BaseModule):

    is_act = True
    button_list = []

    def __init__(self):
        print("初始化手机刺探模块")

    def fram_update(self):
        # self.button_list.clear()
        huo = pyautogui.locateOnScreen("image\\sjct_huo.png")
        if huo and "火" not in self.button_list:
            self.button_list.append("火")
        mu = pyautogui.locateOnScreen("image\\sjct_mu.png")
        if mu and "木" not in self.button_list:
            self.button_list.append("木")
        shui = pyautogui.locateOnScreen("image\\sjct_shui.png")
        if shui and "水" not in self.button_list:
            self.button_list.append("水")
        jin = pyautogui.locateOnScreen("image\\sjct_jin.png")
        if jin and "金" not in self.button_list:
            self.button_list.append("金")
        tu = pyautogui.locateOnScreen("image\\sjtc_tu.png")
        if tu and "土" not in self.button_list:
            self.button_list.append("土")
        if self.button_list:
            print(self.button_list)