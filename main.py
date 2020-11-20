import importlib
import argparse
from lib.gui_controls import Controls
import os
import time
import threading
import lib.global_data as gbd
import lib.version_authentication as va
import ctypes
import win32con
import ctypes.wintypes
import datetime
import lib.windows_con as win_con
import lib
import json
from loguru import logger


class Hotkey(threading.Thread):
    def run(self):
        global EXIT
        user32 = ctypes.windll.user32
        if not user32.RegisterHotKey(None, 99, win32con.MOD_WIN, win32con.VK_F3):
            raise RuntimeError
        try:
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    if msg.wParam == 99:
                        EXIT = False
                        return
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            user32.UnregisterHotKey(None, 1)


def log_init(level="DEBUG"):
    logger.add(
        "log\\runtime_{time}.log", retention="10 days", rotation="5 MB", level=level
    )


def main():
    with open("config\\config.json", "r") as f:
        config = json.loads(f.read())
    if config == "" or config is None:
        logger.error("未找到配置文件")
        return
    log_init(config["log_level"])
    version_data = va.get_version()
    if version_data == None:
        logger.error("版本号异常")
        return
    version = version_data.get("version")
    end_time = version_data.get("end_time")
    if end_time == None:
        logger.error("时间异常")
        return
    time_now = datetime.datetime.now()
    time_now = time_now.year * 1000 + time_now.month * 100 + time_now.day
    if time_now > end_time:
        logger.error("有效期结束")
        return
    logger.info("当前程序版本号：：：" + config["version"])
    logger.info("设置九阴窗口")
    import game_robot

    global EXIT
    Hk = Hotkey()
    Hk.start()
    controls = Controls()
    while EXIT:
        try:
            win_con.set_windwos()
            controls.get_screen()
            for m in gbd.module_dc.values():
                if m.is_act:
                    m.fram_update()
            controls.screen_close()
        except Exception as e:
            logger.error(str(e))
        time.sleep(0.1)


if __name__ == "__main__":
    # path = "GameRobot/chuanqi_web/script"
    EXIT = True
    main()
    input()
