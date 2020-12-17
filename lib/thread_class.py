import lib.global_data as gbd
from lib.gui_controls import Controls
from loguru import logger
import lib.windows_con as win_con
import time
from lib.web_socket import WebSocketClient
from PyQt5.QtCore import QThread,pyqtSignal

class ThreadBase(QThread):
    
    @staticmethod
    def class_name():
        return "ThreadBase"

    def stop(self):
        logger.info(self.class_name()+"线程结束")

class MainRefresh(ThreadBase):

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
                    if gbd.main_window_hwnd == hwnd:
                        continue
                    controls.get_screen(hwnd)
                    for m in gbd.module_dc.values():
                        if m.is_act:
                            m.fram_update(hwnd)
            except Exception as e:
                logger.error(str(e))
            self.msleep(int(gbd.threa_sleep_time*100))

    def stop(self):
        self.is_run = False

    @staticmethod
    def class_name():
        return "MainRefresh"

class WebSocketThread(ThreadBase):
    
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

class KeyRangeThread(ThreadBase):

    thread_done = pyqtSignal()
    run_num = 0
    hwnd = 0
    def __init__(self,hwnd,run_times):
        super(KeyRangeThread, self).__init__()
        self.run_num = run_times
        self.hwnd = hwnd

    def run(self):
        Controls.activate_hwnd(self.hwnd)
        for _ in range(self.run_num):
            for key in gbd.key_range_list:
                Controls.key_post(self.hwnd,key)
            self.msleep(100)
        self.thread_done.emit()
        self.sleep(1)

    @staticmethod
    def class_name():
        return "KeyRange"