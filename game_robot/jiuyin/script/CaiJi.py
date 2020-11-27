from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import pyautogui
from loguru import logger
import win32gui, win32con, win32api

# 采集
class CaiJi(BaseModule):

    is_act = True

    def __init__(self):
        logger.info("初始化采集模块")

    def update_hwnd(self,hwnd):
        up = Controls.locate("image\\ng_jxxl.png", hwnd)
        if up:
            pyautogui.leftClick(up)
            logger.info("继续修炼")