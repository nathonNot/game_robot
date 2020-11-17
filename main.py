import importlib
import argparse
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
# 快捷键线程

class Hotkey(threading.Thread):

    def run(self):
        global EXIT
        user32 = ctypes.windll.user32
        if not user32.RegisterHotKey(None, 99, win32con.MOD_WIN, win32con.VK_F3):
            raise RuntimeError
        try:
            msg = ctypes.wintypes.MSG()
            print(msg)
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
    time_now = time_now.year * 1000 + time_now.month*100 + time_now.day
    if time_now > end_time:
        print("有效期结束")
        return
    print(f"当前程序版本号：：：{version}")
    print("设置九阴窗口")
    win_con.set_windwos()
    import game_robot
    EXIT = True
    Hk = Hotkey()
    Hk.start()
    while(EXIT):
        for m in gbd.module_dc.values():
            if m.is_act:
                m.fram_update()
        time.sleep(0.2)


if __name__ == '__main__':
    # path = "GameRobot/chuanqi_web/script"
    main()
    input()
