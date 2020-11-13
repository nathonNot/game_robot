
from lib.BaseModule import BaseModule
import lib.gui_controls as controls

# 团练授业
class TuanLian(BaseModule):

    is_act = True
    
    def __init__(self):
        print("初始化团练授业模块")

    def fram_update(self):
        print("do update")
        up = controls.get_screen_box("image\\up.png")
        down = controls.get_screen_box("image\\down.png")
        if up:
            print(up)
        if down:
            print(down)
