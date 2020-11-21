import threading
import lib.global_data as gbd
import ctypes
import win32con
import ctypes.wintypes
import threading
from lib.gui_controls import Controls
from loguru import logger
import lib.windows_con as win_con
import time


class Hotkey(threading.Thread):
    def run(self):
        user32 = ctypes.windll.user32
        if not user32.RegisterHotKey(None, 99, win32con.MOD_WIN, win32con.VK_F3):
            raise RuntimeError
        try:
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    if msg.wParam == 99:
                        gbd.Exit = False
                        return
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            user32.UnregisterHotKey(None, 1)


class MainRefresh(threading.Thread):

    def run(self):
        controls = Controls()
        while gbd.Exit:
            try:
                win_con.set_windwos()
                controls.get_screen()
                for m in gbd.module_dc.values():
                    if m.is_act:
                        m.fram_update()
                controls.screen_close()
            except Exception as e:
                logger.error(str(e))
            time.sleep(gbd.threa_sleep_time)