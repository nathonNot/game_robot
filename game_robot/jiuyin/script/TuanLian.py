from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import win32con
from loguru import logger
from lib import global_data as gbd

# 团练授业
class TuanLian(BaseModule):


    # TODO
    # https://gitee.com/AiPandaBear/opencv-python4qqx5/blob/master/rectcheck.py
    
    is_act = False

    onec_button = []
    chick_button = None

    def __init__(self):
        logger.info("初始化团练授业模块")
        self.config = gbd.config_dc["tuan_lian"]
        
    def update_hwnd(self, hwnd):
        # 获取窗口左上角和右下角坐标
        self.onec_button.clear()
        x,y = Controls.get_offset()
        form = (230,440,340,45)
        # up = Controls.localall("image\\tl_up.png", hwnd,self.config["up"],region = form)
        # down = Controls.localall("image\\tl_down.png", hwnd,self.config["down"],region = form)
        # right = Controls.localall("image\\tl_right.png", hwnd,self.config["right"],region = form)
        # left = Controls.localall("image\\tl_left.png", hwnd,self.config["left"],region = form)
        # tl_k = Controls.localall("image\\tl_k.png", hwnd,self.config["k"],region = form)
        # tl_j = Controls.localall("image\\tl_j.png", hwnd,self.config["j"],region = form)
        up = Controls.get_tuanlian_box("image\\tl_up.png", hwnd,self.config["up"],region = form)
        down = Controls.get_tuanlian_box("image\\tl_down.png", hwnd,self.config["down"],region = form)
        right = Controls.get_tuanlian_box("image\\tl_right.png", hwnd,self.config["right"],region = form)
        left = Controls.get_tuanlian_box("image\\tl_left.png", hwnd,self.config["left"],region = form)
        tl_k = Controls.get_tuanlian_box("image\\tl_k.png", hwnd,self.config["k"],region = form)
        tl_j = Controls.get_tuanlian_box("image\\tl_j.png", hwnd,self.config["j"],region = form)
        if up:
            self.add_button_cilck(up, "up", win32con.VK_UP)
        if down:
            self.add_button_cilck(down, "down", win32con.VK_DOWN)
        if right:
            self.add_button_cilck(right, "right", win32con.VK_RIGHT)
        if left:
            self.add_button_cilck(left, "left", win32con.VK_LEFT)
        if tl_k:
            self.add_button_cilck(tl_k, "k", 0x4B)
        if tl_j:
            self.add_button_cilck(tl_j, "j", 0x4A)
        last_x = 0
        if len(self.onec_button) > 0:
            self.de_repetition()
            logger.info(self.onec_button)
            self.set_log(self.get_log_data())
            Controls.activate_hwnd(hwnd)
            for key in self.onec_button:
                # if (key[1] - last_x) <= 5:
                #     continue
                Controls.key_post(hwnd, key[2])
                last_x = key[1]

    def add_button_cilck(self, button_find, button_name, vk_key):
        for button in button_find:
            if button is None:
                continue
            new_list = [button_name, button.left, vk_key]
            if new_list in self.onec_button:
                continue
            self.onec_button.append(new_list)
            self.chick_button = button

    def de_repetition(self):
        self.onec_button.sort(key=lambda x: x[1])
        new_list = []
        for i in range(len(self.onec_button)):
            if self.onec_button[i] in new_list:
                continue
            if len(self.onec_button) > i+1:
                if (self.onec_button[i+1][1] - self.onec_button[i][1])<7:
                    continue
            new_list.append(self.onec_button[i])
        self.onec_button = new_list
    
    def get_log_data(self):
        log_data = []
        for bt in self.onec_button:
            if bt[0] == "right":
                log_data.append("右")
            if bt[0] == "down":
                log_data.append("下")
            if bt[0] == "left":
                log_data.append("左")
            if bt[0] == "up":
                log_data.append("上")
            if bt[0] == "j":
                log_data.append("j")
            if bt[0] == "k":
                log_data.append("k")
        return ",".join(log_data)