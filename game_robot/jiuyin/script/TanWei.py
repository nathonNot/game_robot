from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
from loguru import logger

# 刷摊位
class TanWei(BaseModule):

    is_act = False
    is_vip = False

    def __init__(self):
        logger.info("初始化摊位模块")
    

    def update_hwnd(self,hwnd):
        queding = Controls.locate("image\\tw_queding.png", hwnd,0.8)
        if queding:
            Controls.win_mouse_click_box(hwnd,queding,True,0.1)
            return
        tanwei = Controls.locate("image\\tw_lxbt.png", hwnd,0.8)
        if tanwei:
            Controls.win_mouse_click_box(hwnd,tanwei,True,0.1)
        else:
            Controls.activate_hwnd(hwnd)
            Controls.key_post(hwnd, 0x50,1)
