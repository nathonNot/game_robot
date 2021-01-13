from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
from loguru import logger
import time

# 采集
class CaiJi(BaseModule):

    is_act = False
    this_x = 650
    this_y = 95

    map_pos = [
        
    ]


    def __init__(self):
        logger.info("初始化采集模块")

    def update_hwnd(self,hwnd):
        if self.this_x <= 700 and self.this_x >= 650:
            self.this_x += 5
        else:
            self.this_x = 650
        get_item = Controls.locate("image\\cj_miaoshu.png", hwnd,0.05)
        if get_item:
            Controls.win_mouse_click(hwnd,self.this_x,self.this_y)
            logger.info("获取采集")
            time.sleep(3)
