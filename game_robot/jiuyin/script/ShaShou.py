from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import pyautogui
from loguru import logger

# 杀手
class ShaShou(BaseModule):

    is_act = True

    def __init__(self):
        logger.info("初始化杀手模块")

    def update_hwnd(self,hwnd):
        tiezi = Controls.locate("image\\ss_tiezi.png", hwnd)
        if tiezi:
            print(tiezi)
            Controls.win_mouse_click(hwnd,tiezi.left,tiezi.top)
            logger.info("打开杀手帖子")
        jieshou = Controls.locate("image\\ss_jieshou.png", hwnd)
        if jieshou:
            x = jieshou.left + jieshou.width/2
            y = jieshou.top + jieshou.height/2
            Controls.win_mouse_move(hwnd,0,0)
            # pyautogui.moveTo(jieshou)
            for _ in range(5):
                Controls.win_mouse_move(hwnd,jieshou.left,jieshou.top,0)
                Controls.win_mouse_click(hwnd,jieshou.left,jieshou.top,0)
            Controls.win_mouse_click(hwnd,jieshou.left,jieshou.top)
            logger.info("接受杀手邀请")