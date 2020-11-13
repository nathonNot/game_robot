
from lib.BaseModule import BaseModule
import lib.gui_controls as controls
import pyautogui

# 团练授业
class TuanLian(BaseModule):

    is_act = True
    
    onec_button = []
    chick_button = None

    def __init__(self):
        print("初始化团练授业模块")

    def fram_update(self):
        print("do update")
        self.onec_button.clear()
        up = controls.get_screen_box_all("image\\tl_up.png")
        down = controls.get_screen_box_all("image\\tl_down.png")
        right = controls.get_screen_box_all("image\\tl_right.png")
        left = controls.get_screen_box_all("image\\tl_left.png")
        tl_k = controls.get_screen_box_all("image\\tl_k.png")
        tl_j = controls.get_screen_box_all("image\\tl_j.png")
        if up:
            for u in up:
                self.onec_button.append(["up",u.left])
                self.chick_button = u
        if down:
            for d in down:
                self.onec_button.append(["down",d.left])
                self.chick_button = d
        if right:
            for r in right:
                self.onec_button.append(["right",r.left])
                self.chick_button = r
        if left:
            for l in left:
                self.onec_button.append(["left",l.left])
                self.chick_button = l
        if tl_k:
            for k in tl_k:
                self.onec_button.append(["k",k.left])
                self.chick_button = k
        if tl_j:
            for j in tl_j:
                self.onec_button.append(["j",j.left])
                self.chick_button = j
        if len(self.onec_button) >0:
            self.onec_button.sort(key = lambda x: x[1])
            print(self.onec_button)
            pyautogui.leftClick(self.chick_button)
            for key in self.onec_button:
                pyautogui.press(key[0])
            
