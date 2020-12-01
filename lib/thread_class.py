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
from lib.web_socket import WebSocketClient

class MainRefresh(threading.Thread):

    is_run = False

    def run(self):
        controls = Controls()
        self.is_run = True
        while self.is_run:
            try:
                win_con.set_windwos()
                if len(gbd.hwnd_list) <= 0:
                    return
                for hwnd in gbd.hwnd_list:
                    controls.get_screen(hwnd)
                    for m in gbd.module_dc.values():
                        if m.is_act:
                            m.fram_update(hwnd)
            except Exception as e:
                logger.error(str(e))
            time.sleep(gbd.threa_sleep_time)

    def stop(self):
        self.is_run = False

    @staticmethod
    def class_name():
        return "MainRefresh"

class WebSocketThread(threading.Thread):
    
    ws = None

    def run(self):
        self.ws = WebSocketClient()
        self.ws.do_login()
    
    def stop(self):
        if self.ws == None:
            return
        self.ws.client.close()

    @staticmethod
    def class_name():
        return "WebSocketThread"