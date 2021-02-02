from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
from loguru import logger
from lib.utils import win_key_dc

# 弹琴
class TanQin(BaseModule):

    is_act = True
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

    button_from = {}

    def __init__(self):
        logger.info("初始化自动弹琴")

    def fram_update(self,hwnd):
        Controls.activate_hwnd(hwnd)
        Controls.key_post(hwnd,win_key_dc["6"],0.2)
        # gbd.hwnd_work_dc[hwnd].activate_hwnd(hwnd)
        self.check_button(hwnd)
        self.flush_button(hwnd)
        Controls.un_activate_hwnd(hwnd)

    def check_button(self,hwnd):
        fm = [440,400,330,150]
        if len(self.button_img) > 4:
            self.button_from.clear()
        for button,img in self.button_img.items():
            button_box = Controls.locate(img,hwnd,0.98,fm)
            if button_box:
                self.button_from[button] = [button_box.left-30,button_box.top,button_box.width+10,button_box.height]

    def flush_button(self,hwnd):
        for button,button_from in self.button_from.items():
            Controls.get_screen(hwnd)
            is_enter = Controls.locate("image\\tq_blue.png",hwnd,0.5,button_from)
            if is_enter:
                Controls.key_post(hwnd,win_key_dc[button],1)
                print(button)