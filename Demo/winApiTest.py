from traceback import print_tb
import win32api
import win32gui
import win32con  # 导入win32api相关模块
import time
import cv2
import numpy as np
from PIL import Image
import collections
from gui_controls import Controls

def get_hwnd():
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    ret_hwnd = 0
    for hwnd in hWndList:
        title = win32gui.GetWindowText(hwnd)
        # 调整目标窗口到坐标(600,300),大小设置为(600,600)
        if (title.find("九阴真经 江湖") >= 0) or (title.find("九阴真经") >= 0):
            print(hwnd, title)
            if hwnd > 0:
                ret_hwnd = hwnd
    return ret_hwnd


Box = collections.namedtuple('Box', 'left top width height')
# k 0x4B
# j 0x4A
# win32con.VK_LEFT 左
# VK_UP 上
# VK_RIGHT 右
# VK_DOWN 下
# win32api.PostMessage(8915604, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)#发送F9键
# win32api.PostMessage(8915604, win32con.WM_KEYUP, win32con.VK_LEFT, 0)

# 按钮点击


def test_done1():
    win32api.PostMessage(200352, win32con.WM_LBUTTONDOWN, 1, 0x003002F3)
    time.sleep(1)
    win32api.PostMessage(200352, win32con.WM_LBUTTONUP, 1, 0x003002F3)


# 按钮点击
def mouse_click(hwnd,x, y):
    point = win32api.MAKELONG(x, y)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, point)
    time.sleep(1)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 1, point)

# 窗口最大最小化
def window_test(hwnd):
    _, win_type, _, _, _ = win32gui.GetWindowPlacement(hwnd)
    print(win_type)


def get_hwnd_offset(hwnd,x,y):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return x+left,y+top

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


def move_to_pos(hwnd,x,y):
    # 出发地图键m
    Controls.activate_hwnd(hwnd)
    # 视角距离滑动拉到最近
    # Controls.win_gunlun_qian(hwnd)
    # Controls.key_post(hwnd,0x4D)
    # # x,y = get_hwnd_offset(hwnd,115,34)
    # Controls.win_mouse_click(hwnd,115,34)
    # input_hwnd(hwnd,[0x35,0x39,0x31])
    # Controls.win_mouse_click(hwnd,185,40)
    # input_hwnd(hwnd,[0x32,0x32,0x36])
    # Controls.win_mouse_click(hwnd,223,33)
    # time.sleep(1)
    # Controls.win_mouse_click(hwnd,320,274)
    # # 关闭地图
    # Controls.key_post(hwnd,0x4D)
    # # 移动到拉镖点
    # time.sleep(2)
    box = check(hwnd)
    Controls.win_mouse_move(hwnd,700,93)
    time.sleep(1)
    Controls.win_mouse_click(hwnd,700,93)
    time.sleep(1)
    # Controls.win_mouse_click(hwnd,150,221)
    # Controls.get_screen(hwnd)
    box = Controls.locate2("D:\project\python\jiuyin_robot\image\lb_jiebiao.png")
    # if box:
    #     print("接镖1")
    #     Controls.win_mouse_move(hwnd,244,479)
        # Controls.win_mouse_click(hwnd,244,479)
    # Controls.get_screen(hwnd)
    # biaoche = Controls.locate2("D:\project\python\jiuyin_robot\image\lb_jiebiaot.png",0.5)
    # if biaoche:
    #     print("接镖2")
    #     Controls.win_mouse_move(hwnd,658,492)
    #     Controls.win_mouse_click(hwnd,658,492)
    # time.sleep(0.2)
    # Controls.get_screen(hwnd)
    # queding = Controls.locate2("D:\project\python\jiuyin_robot\image\lb_queding.png")
    # if queding:
    #     print("确定接镖")
    #     Controls.win_mouse_move(hwnd,398,342)
    #     Controls.win_mouse_click(hwnd,398,342)
    Controls.get_screen(hwnd)
    # jiache = Controls.locate2("D:\project\python\jiuyin_robot\image\lb_jiache.png")
    # if jiache:
    #     print("选择驾车")
    #     x,y = get_xy(jiache)
    #     Controls.win_mouse_click(hwnd,x,y)
    status = Controls.locate("D:\project\python\jiuyin_robot\image\lb_icon.png")
    if status:
        print("拉镖状态ok")

def get_xy(box):
    x = box.left + box.width/2
    y = box.top - box.height
    return int(x), int(y)

def check(hwnd):
    offset = (650,50,100,50)
    while True:
        for x in range(695,710):
            for y in range(85,100):
                Controls.win_mouse_move(hwnd,x,y,0.1)
                Controls.get_screen(hwnd)
                box = Controls.locate("D:\project\python\jiuyin_robot\image\lb_jiangliefeng.png",0.3)
                if box:
                    return box

# 闪烁窗口
def fluash_hwnd(hwnd):
    win32gui.FlashWindowEx(hwnd,True,5,0)

def tanwei(hwnd):
    point = win32api.MAKELONG(479, 344)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, point)
    time.sleep(0.2)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 1, point)

def anjian(hwnd):
    Controls.activate_hwnd(hwnd)
    Controls.key_post(hwnd, 0x68)
    for _ in range(100):
        Controls.key_post(hwnd, 56)
        time.sleep(0.1)

if __name__ == "__main__":
    hwnd = get_hwnd()
    move_to_pos(hwnd,0,0)
    # anjian(hwnd)
    # win32api.MessageBox(0, "这是一个测试消息", "消息框标题",win32con.MB_OK)