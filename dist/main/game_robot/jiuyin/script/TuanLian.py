
from lib.BaseModule import BaseModule
from lib.gui_controls import controls
import pyautogui

# 团练授业
class TuanLian(BaseModule):

    is_act = True
    
    onec_button = []
    chick_button = None

    def __init__(self):
        print("初始化团练授业模块")

    def fram_update(self):
        print("扫描")
        self.onec_button.clear()
        up = controls.get_screen_box_all("image\\tl_up.png")
        down = controls.get_screen_box_all("image\\tl_down.png")
        right = controls.get_screen_box_all("image\\tl_right.png")
        left = controls.get_screen_box_all("image\\tl_left.png")
        tl_k = controls.get_screen_box_all("image\\tl_k.png")
        tl_j = controls.get_screen_box_all("image\\tl_j.png")
        if up:
            self.add_button_cilck(up,"up")
        if down:
            self.add_button_cilck(down,"down")
        if right:
            self.add_button_cilck(right,"right")
        if left:
            self.add_button_cilck(left,"left")
        if tl_k:
            self.add_button_cilck(tl_k,"k")
        if tl_j:
            self.add_button_cilck(tl_j,"j")
        if len(self.onec_button) >0:
            self.onec_button.sort(key = lambda x: x[1])
            print(self.onec_button)
            pyautogui.leftClick(self.chick_button)
            for key in self.onec_button:
                pyautogui.press(key[0])
    

    def add_button_cilck(self,button_find,button_name):
        for button in button_find:
            self.onec_button.append([button_name,button.left])
            self.chick_button = button