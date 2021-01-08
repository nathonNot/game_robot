import lib.global_data as gbd
from lib.gui_controls import Controls
from loguru import logger
import lib.windows_con as win_con
import time
from lib.web_socket import WebSocketClient
from PyQt5.QtCore import QThread,pyqtSignal
import threading

class ThreadBase(QThread):
    
    @staticmethod
    def class_name():
        return "ThreadBase"

    def stop(self):
        logger.info(self.class_name()+"线程结束")

class MainRefresh(ThreadBase):
# class MainRefresh(threading.Thread):

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
                        if m.is_vip:
                            if not gbd.user_data.is_vip():
                                continue
                        if m.is_act:
                            m.fram_update(hwnd)
                # self.msleep(200)
                time.sleep(0.2)
            except Exception as e:
                logger.error(str(e))

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
    def __init__(self,hwnd,run_times,sleep_times):
        super(KeyRangeThread, self).__init__()
        self.run_num = run_times
        self.hwnd = hwnd
        self.sleep_times = sleep_times

    def run(self):
        for _ in range(self.run_num):
            if len(gbd.key_range_list) <= 0:
                break
            for key in gbd.key_range_list:
                Controls.activate_hwnd(self.hwnd)
                Controls.key_post(self.hwnd,key)
                Controls.un_activate_hwnd(self.hwnd)
                self.msleep(self.sleep_times)
        self.thread_done.emit()
        # self.sleep(1)

    @staticmethod
    def class_name():
        return "KeyRange"