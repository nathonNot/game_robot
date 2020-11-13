import importlib
import argparse
import os
import time
import threading
from lib.BaseModule import BaseModule
from lib.utils import init_file
import lib.global_data as gbd
import ctypes, win32con, ctypes.wintypes, win32gui

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



if __name__ == '__main__':
    # path = "GameRobot/chuanqi_web/script"
    path = "GameRobot/jiuyin/script"
    init_file(path)
    EXIT = True
    Hk = Hotkey()
    Hk.start()
    while(EXIT):
        for m in gbd.module_dc.values():
            if m.is_act:
                m.fram_update()
        time.sleep(1)
