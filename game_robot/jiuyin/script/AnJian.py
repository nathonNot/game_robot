from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
from loguru import logger


# 按键连按
class AnJian(BaseModule):

    is_act = False

    def __init__(self):
        logger.info("初始化按键连按")

    def fram_update(self,hwnd):
        Controls.activate_hwnd(hwnd)
        for _ in range(10):
            Controls.key_post(hwnd, 56)
            # Controls.key_post(hwnd, 52)