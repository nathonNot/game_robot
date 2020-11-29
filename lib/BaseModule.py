from loguru import logger
from lib import global_data

class BaseModule:

    is_act = True

    def __init__(self):
        pass

    @logger.catch
    def fram_update(self,hwnd):
        self.update_hwnd(hwnd)
    
    def update_hwnd(self,hwnd):
        pass

    def set_log(self,log_info):
        if global_data.main_log_info_call_back is None:
            return
        global_data.main_log_info_call_back(log_info)