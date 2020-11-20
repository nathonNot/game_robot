from loguru import logger
from lib import global_data

class BaseModule:

    is_act = True

    def __init__(self):
        pass

    @logger.catch
    def fram_update(self):
        if len(global_data.hwnd_list) <= 0:
            return
        for hwnd in global_data.hwnd_list:
            self.update_hwnd(hwnd)
    
    def update_hwnd(self,hwnd):
        pass