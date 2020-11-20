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

# 快捷键线程


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


def main():
    with open("config\\config.json", "r") as f:
        config = json.loads(f.read())
    if config == "" or config is None:
        print("未找到配置文件")
        return

    version_data = va.get_version()
    if version_data == None:
        print("版本号异常")
        return
    version = version_data.get("version")
    end_time = version_data.get("end_time")
    if end_time == None:
        print("时间异常")
        return
    time_now = datetime.datetime.now()
    time_now = time_now.year * 1000 + time_now.month * 100 + time_now.day
    if time_now > end_time:
        print("有效期结束")
        return
    print("当前程序版本号：：：" + config["version"])
    print("设置九阴窗口")
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
            print(str(e))
        time.sleep(0.1)


if __name__ == "__main__":
    # path = "GameRobot/chuanqi_web/script"
    EXIT = True
    main()
    input()
