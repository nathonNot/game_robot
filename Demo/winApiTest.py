import win32api
import win32gui
import win32con  # 导入win32api相关模块
import time
import pyautogui
import cv2
import numpy as np
from PIL import Image


def get_hwnd():
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    ret_hwnd = 0
    for hwnd in hWndList:
        title = win32gui.GetWindowText(hwnd)
        # 调整目标窗口到坐标(600,300),大小设置为(600,600)
        if (title.find("九阴真经  江湖") >= 0) or (title.find("九阴真经  武侠") >= 0):
            print(hwnd, title)
            if hwnd > 0:
                ret_hwnd = hwnd
    return ret_hwnd

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


def mouse_click(x, y):
    point = win32api.MAKELONG(x, y)
    win32api.PostMessage(200352, win32con.WM_LBUTTONDOWN, 1, point)
    time.sleep(1)
    win32api.PostMessage(200352, win32con.WM_LBUTTONUP, 1, point)

# 测试，屏幕截屏相关api


def test_screen():
    # screen = pyautogui.screenshot()
    import win32gui
    import win32ui
    w = 800
    h = 600
    hwnd = get_hwnd()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bottom - top
    bmpfilenamename = "jiuyin.png"
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)
    image = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    # image = cv2.imread(bmpfilenamename)
    locat = pyautogui.locate(
        "D:\\project\\python\\jiuyin_robot\\image\\chengdu.png", image, confidence=0.8)
    print(locat)
    offset_x = locat.left
    offset_y = locat.top
    window_x = left + offset_x
    window_y = top + offset_y
    if not locat is None:
        pyautogui.rightClick(x=window_x, y=window_y)


if __name__ == '__main__':
    test_screen()
