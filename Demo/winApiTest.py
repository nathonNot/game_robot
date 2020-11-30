from traceback import print_tb
import win32api
import win32gui
import win32con  # 导入win32api相关模块
import time
import pyautogui
import cv2
import numpy as np
from PIL import Image
import collections

def get_hwnd():
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    ret_hwnd = 0
    for hwnd in hWndList:
        title = win32gui.GetWindowText(hwnd)
        # 调整目标窗口到坐标(600,300),大小设置为(600,600)
        if (title.find("111.txt") >= 0) or (title.find("九阴真经  武侠") >= 0):
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
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
    )

    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    # image = cv2.imread(bmpfilenamename)
    locat = pyautogui.locate(
        "D:\\project\\python\\jiuyin_robot\\image\\chengdu.png", image, confidence=0.8
    )
    print(locat)
    offset_x = locat.left
    offset_y = locat.top
    window_x = left + offset_x
    window_y = top + offset_y
    if not locat is None:
        pyautogui.rightClick(x=window_x, y=window_y)


# 窗口最大最小化
def window_test(hwnd):
    _, win_type, _, _, _ = win32gui.GetWindowPlacement(hwnd)
    print(win_type)

# 图形识别
def map_read_test(base_map,t_map,rate):
    """
    base_map  基底图
    t_map     匹配图
    rate      匹配率
    """
    img_rgb = cv2.imread(base_map) 
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 
    template = cv2.imread(t_map,0)
    # cv2.imshow('rgb',img_rgb)
    # cv2.imshow('gray',img_gray)
    # cv2.imshow('template',template)
    w, h = template.shape[::-1] 
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) 
    threshold = rate 
    loc = np.where( res >= threshold) 
    for pt in zip(*loc[::-1]): 
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)    
    # cv2.imshow('Detected',img_rgb) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 
    region = (0, 0)
    match_indices = np.arange(res.size)[(res > threshold).flatten()]
    matches = np.unravel_index(match_indices[:10000], res.shape)

    # use a generator for API consistency:
    matchx = matches[1] * 1 + region[0]  # vectorized
    matchy = matches[0] * 1 + region[1]
    needleHeight, needleWidth = img_rgb.shape[:2]

    for x, y in zip(matchx, matchy):
        box = Box(x, y, needleWidth, needleHeight)
        print(box)

if __name__ == "__main__":
    base_map = "image\\tl_k.png"
    t_map = "image\\tl_k1.png"
    rate = 0.8
    map_read_test(base_map,t_map,rate)