import pyautogui
import win32api,win32gui,win32ui
import win32con  # 导入win32api相关模块
import time
from PIL import Image

class Controls:

    screen = None
    form = None
    offset_left = 0
    offset_right = 0
    offset_top = 0
    offset_bottom = 0

    @classmethod
    def get_screen(cls,hwnd):
        # cls.screen = pyautogui.screenshot()
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        cls.offset_left = left
        cls.offset_right = right
        cls.offset_bottom = bottom
        cls.offset_top = top
        w = right - left
        h = bottom - top
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
        # bmpfilenamename = "jiuyin.png"
        # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        # 清理内存
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        cls.screen = image

    @classmethod
    def localall(cls, path, hwnd, contrast_ratio=0.9,offset_form=None):
        locat_all = []
        all_list = pyautogui.locateAll(
            path, cls.screen,confidence=contrast_ratio
        )
        if not all_list:
            return []
        for box in all_list:
            if box is None:
                return []
            locat_all.append(cls.offset_box(box))
        return locat_all

    @classmethod
    def locate(cls, path, hwnd, contrast_ratio=0.9):
        loca_box = pyautogui.locate(path, cls.screen,confidence=contrast_ratio)
        return cls.offset_box(loca_box)

    @classmethod
    def offset_box(cls,box):
        if box is None:
            return None
        new_left = box.left + cls.offset_left
        new_top = box.top + cls.offset_top
        box._replace(left=new_left)
        box._replace(top=new_top)
        return box

    # 路径，对比度
    @staticmethod
    def get_screen_box(path, contrast_ratio=0.9):
        return pyautogui.locateOnScreen(path, confidence=contrast_ratio)

    # 右键单击,路径中不能有中文
    @staticmethod
    def right_click(path):
        coords = Controls.get_screen_box(path)
        if coords:
            # 获取定位到的图中间点坐标
            x, y = pyautogui.center(coords)
            # 右击该坐标点
            pyautogui.rightClick(x, y)
            return True
        return False

    # 左键单击,路径中不能有中文
    @staticmethod
    def left_click(path):
        coords = Controls.get_screen_box(path)
        if coords:
            print("找到" + path)
            # 获取定位到的图中间点坐标
            x, y = pyautogui.center(coords)
            # 右击该坐标点
            pyautogui.leftClick(x, y)
            return True
        return False

    @staticmethod
    def activate_hwnd(hwnd):
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATEAPP, 0x1, 0)
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATE, 0x2, 0)
        win32api.SendMessage(hwnd, win32con.WM_IME_SETCONTEXT, 0x1, 0xC000000F)
        win32api.SendMessage(hwnd, win32con.WM_IME_NOTIFY, 0x2, 0)

    # 键盘摁下抬起
    @staticmethod
    def key_post(hwnd, key):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0x2E0001)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0x2E0001)

    # 直接发起鼠标点击，走windows窗口事件
    @staticmethod
    def win_mouse_click(hwnd, x, y, sleep_time=1):
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, point)
        time.sleep(sleep_time)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 1, point)

    @staticmethod
    def win_mouse_move(hwnd, x, y, sleep_time=1):
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, point)
        time.sleep(sleep_time)
