from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import pyautogui
from loguru import logger

# 内功
class NeiGong(BaseModule):

    is_act = True

    def __init__(self):
        logger.info("初始化内功模块")

    def update_hwnd(self,hwnd):
        # 获取窗口左上角和右下角坐标
        xleft, ytop, xright, ybottom = win32gui.GetWindowRect(hwnd)
        form = (xleft, ytop, (xright - xleft), (ybottom - ytop))
        up = Controls.locate("image\\ng_jxxl.png", form)
        if up:
            pyautogui.leftClick(up)
            logger.info("继续修炼")