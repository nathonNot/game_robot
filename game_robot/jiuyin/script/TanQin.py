from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
from loguru import logger
from lib.utils import win_key_dc,win_key_up_iparam_dc
import win32api
import win32con
import time

# 弹琴
class TanQin(BaseModule):

    is_act = False
    button_img = {
        "c":"image\\tq_c.png",
        "d":"image\\tq_d.png",
        "i":"image\\tq_i.png",
        "l":"image\\tq_l.png",
        "o":"image\\tq_o.png",
        "p":"image\\tq_p.png",
        "s":"image\\tq_s.png",
        "a":"image\\tq_a.png",
        "x":"image\\tq_x.png",
        "j":"image\\tq_j.png",
        "k":"image\\tq_k.png",
    }
    fm = [440,400,360,150]

    button_from = {}

    def __init__(self):
        logger.info("初始化自动弹琴")

    def fram_update(self,hwnd):
        self.check_start(hwnd)
        self.check_button(hwnd)
        self.flush_button(hwnd)

    '''
    是否在弹琴状态
    不在的时候重新启动
    然后清空一次按钮列
    '''
    def check_start(self,hwnd):
        button_box = Controls.locate("image\\tq_button.png",hwnd,0.5,self.fm)
        if button_box is None:
            self.button_from.clear()
            self.set_log("重启弹琴")
            time.sleep(2)
            Controls.activate_hwnd(hwnd)
            Controls.key_post(hwnd,win_key_dc["6"],0.2)
            Controls.un_activate_hwnd(hwnd)

    def check_button(self,hwnd):
        if len(self.button_from) == 4:
            return
        for button,img in self.button_img.items():
            button_box = Controls.locate(img,hwnd,0.98,self.fm)
            if button_box:
                self.button_from[button] = [button_box.left-20,button_box.top-3,button_box.width+20,button_box.height+1]

    def flush_button(self,hwnd):
        if len(self.button_from) <= 0:
            return
        Controls.activate_hwnd(hwnd)
        for button,froms in self.button_from.items():
            is_enter = Controls.locate("image\\tq_blue.png",hwnd,0.45,froms)
            if is_enter:
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, win_key_dc[button], win_key_up_iparam_dc[button])
                time.sleep(0.1)
                # Controls.key_post(hwnd,win_key_dc[button],1)
                self.set_log(button)
                self.button_from[button] = froms
        Controls.un_activate_hwnd(hwnd)
