import lib.global_data as gbd
from lib.gui_controls import Controls
from loguru import logger
import lib.windows_con as win_con
import time
from lib.web_socket import WebSocketClient
from PyQt5.QtCore import QThread,pyqtSignal
import threading


class ThreadBase(QThread):
    
    is_run = False
    
    @staticmethod
    def class_name():
        return "ThreadBase"

    def stop(self):
        logger.info(self.class_name()+"线程结束")
        self.is_run = False

class MainRefresh(ThreadBase):
# class MainRefresh(threading.Thread):

    is_run = False
    work_dc = {}

    def run(self):
        self.is_run = True
        gbd.hwnd_work_dc.clear()
        for hwnd in gbd.hwnd_list:
            if hwnd in gbd.main_window_hwnd:
                continue
            self.work_dc[hwnd] = WorkRefresh(hwnd)
            self.work_dc[hwnd].start()
        while self.is_run:
            try:
                win_con.set_windwos()
                if len(gbd.hwnd_list) <= 0:
                    self.stop()
                    return
                self.msleep(500)
                # time.sleep(0.5)
            except Exception as e:
                logger.error(str(e))

    def stop(self):
        self.is_run = False
        for worker in self.work_dc.values():
            worker.stop()

    @staticmethod
    def class_name():
        return "MainRefresh"

# 窗口工作线程，一个窗口对应一个线程
class WorkRefresh(ThreadBase):
# class WorkRefresh(threading.Thread):
    is_run = False
    hwnd = 0
    
    def __init__(self,hwnd):
        super(WorkRefresh, self).__init__()
        self.hwnd = hwnd
        self.controls = Controls(self.is_run)
        gbd.hwnd_work_dc[hwnd] = self.controls

    def run(self):
        self.is_run = True
        while self.is_run:
            try:
                self.controls.is_run = self.is_run
                self.controls.get_screen(self.hwnd)
                for m in gbd.module_dc.values():
                    if m.is_vip:
                        if not gbd.user_data.is_vip():
                            continue
                    if m.is_act:
                        m.fram_update(self.hwnd)
                self.msleep(200)
                time.sleep(0.2)
            except Exception as e:
                logger.error(str(e))

    def stop(self):
        self.is_run = False
        self.controls.is_run = False

    @staticmethod
    def class_name():
        return "WorkRefresh"


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