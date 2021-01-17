from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
from loguru import logger
import time

# 采集
class CaiJi(BaseModule):

    is_act = False

    def __init__(self):
        logger.info("初始化采集模块")

    def update_hwnd(self,hwnd):
        Controls.activate_hwnd(hwnd)
        self.flush(hwnd)
        Controls.un_activate_hwnd(hwnd)
        
    def flush(self,hwnd):
        for x in range(678,726,5):
            if self.check_shiqu(hwnd,x,40):
                return
        for x in range(670,734,5):
            if self.check_shiqu(hwnd,x,50):
                return
        for x in range(650,745,5):
            if self.check_shiqu(hwnd,x,60):
                return
        for x in range(640,750,5):
            if self.check_shiqu(hwnd,x,70):
                return
        for x in range(637,755,5):
            if self.check_shiqu(hwnd,x,80):
                return
        for x in range(637,755,5):
            if self.check_shiqu(hwnd,x,80):
                return
        for x in range(637,750,5):
            if self.check_shiqu(hwnd,x,90):
                return
        for x in range(650,750,5):
            if self.check_shiqu(hwnd,x,100):
                return
        for x in range(638,753,5):
            if self.check_shiqu(hwnd,x,110):
                return
        for x in range(638,753,5):
            if self.check_shiqu(hwnd,x,110):
                return
        for x in range(642,745,5):
            if self.check_shiqu(hwnd,x,120):
                return
        for x in range(653,750,5):
            if self.check_shiqu(hwnd,x,130):
                return
        for x in range(663,730,5):
            if self.check_shiqu(hwnd,x,140):
                return
        for x in range(680,730,5):
            if self.check_shiqu(hwnd,x,150):
                return

    def check_shiqu(self,hwnd,x,y):
        Controls.win_mouse_click(hwnd,x,y)
        Controls.get_screen(hwnd)
        shiqu = Controls.locate("image\cj_shiqu.png",hwnd,0.8)
        if shiqu:
            Controls.win_mouse_click_box(hwnd,shiqu,True)
            return True
        return False