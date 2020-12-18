from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
from loguru import logger

# 杀手
class ShaShou(BaseModule):

    is_act = False
    tiezi_box = None

    def __init__(self):
        logger.info("初始化杀手模块")
    

    def update_hwnd(self,hwnd):
        tiezi = Controls.locate("image\\ss_tiezi.png", hwnd)
        if tiezi:
            Controls.win_mouse_click_box(hwnd,tiezi)
            logger.info("打开杀手帖子")
            self.tiezi_box = tiezi
        jieshou = Controls.locate("image\\ss_jieshou.png", hwnd)
        if jieshou:
            print(jieshou)
            Controls.win_mouse_click_box(hwnd,jieshou,True)
            logger.info("接受杀手邀请")