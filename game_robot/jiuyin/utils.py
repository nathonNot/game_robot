from lib.gui_controls import Controls
import time
import win32api
import win32gui
import win32con  # 导入win32api相关模块
from  lib.utils import win_key_dc

def get_xy(x,y):
    x_list = [win_key_dc[xx] for xx in str(x)]
    y_list = [win_key_dc[yy] for yy in str(y)]
    return x_list,y_list

def move_to_pos(hwnd,x,y):
    # 出发地图键m
    Controls.activate_hwnd(hwnd)
    # 视角距离滑动拉到最近
    Controls.win_gunlun_qian(hwnd)

    Controls.key_post(hwnd,0x4D)
    # x,y = get_hwnd_offset(hwnd,115,34)
    Controls.win_mouse_click(hwnd,115,34)
    input_hwnd(hwnd,x)
    Controls.win_mouse_click(hwnd,185,40)
    input_hwnd(hwnd,y)
    Controls.win_mouse_click(hwnd,223,33)
    time.sleep(1)
    Controls.win_mouse_move(hwnd,316,281,0.5)
    Controls.win_mouse_click(hwnd,316,281)
    # 洛阳
    # Controls.win_mouse_click(hwnd,328,290)
    # 燕京
    # Controls.win_mouse_click(hwnd,331,290)
    # 关闭地图
    Controls.key_post(hwnd,0x4D)
    # # 移动到拉镖点
    # time.sleep(2)
    # box = check(hwnd)
    # print(box)
    # Controls.win_mouse_move(hwnd,700,93)
    # time.sleep(1)
    # Controls.win_mouse_click(hwnd,700,93)
    # time.sleep(1)
    # Controls.win_mouse_click(hwnd,150,221)
    # Controls.get_screen(hwnd)
    # box = Controls.locate2("D:\project\python\jiuyin_robot\image\la_jiebiao.png")
    # if box:
    #     print(box)
    #     Controls.win_mouse_move(hwnd,244,479)
    #     Controls.win_mouse_click(hwnd,244,479)

def input_hwnd(hwnd,input_list):
    # 先删除
    for _ in range(5):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x27, 0x1F0001)
        time.sleep(0.2)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x27, 0x1F0001)
    for _ in range(5):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x8, 0x1F0001)
        time.sleep(0.2)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x8, 0x1F0001)
    for input in input_list:
        win32api.PostMessage(hwnd, win32con.WM_CHAR, input, 0x1F0001)

def check(hwnd):
    while True:
        for x in range(695,700):
            for y in range(88,93):
                Controls.win_mouse_move(hwnd,x,y)
                time.sleep(0.2)
                Controls.get_screen(hwnd)
                box = Controls.locate2("D:\project\python\jiuyin_robot\image\lb_liaocanghai.png",0.5)
                if box:
                    return box