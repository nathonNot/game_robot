from lib.gui_controls import Controls
import time
import win32api
import win32gui
import win32con  # 导入win32api相关模块

def move_to_pos(hwnd,x,y):
    # 出发地图键m
    Controls.activate_hwnd(hwnd)
    # 视角距离滑动拉到最近
    Controls.win_gunlun_qian(hwnd)

    Controls.key_post(hwnd,0x4D)
    # x,y = get_hwnd_offset(hwnd,115,34)
    Controls.win_mouse_click(hwnd,115,34)
    input_hwnd(hwnd,[0x37,0x32,0x32])
    Controls.win_mouse_click(hwnd,185,40)
    input_hwnd(hwnd,[0x35,0x31,0x37])
    Controls.win_mouse_click(hwnd,223,33)
    time.sleep(1)
    Controls.win_mouse_click(hwnd,320,274)
    # 关闭地图
    Controls.key_post(hwnd,0x4D)
    # 移动到拉镖点
    time.sleep(2)
    box = check(hwnd)
    print(box)
    Controls.win_mouse_move(hwnd,700,93)
    time.sleep(1)
    Controls.win_mouse_click(hwnd,700,93)
    time.sleep(1)
    Controls.win_mouse_click(hwnd,150,221)
    Controls.get_screen(hwnd)
    box = Controls.locate2("D:\project\python\jiuyin_robot\image\la_jiebiao.png")
    if box:
        print(box)
        Controls.win_mouse_move(hwnd,244,479)
        Controls.win_mouse_click(hwnd,244,479)

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