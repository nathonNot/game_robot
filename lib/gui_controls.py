from numpy.lib.function_base import kaiser
import win32api
import win32gui
import win32ui
import win32con  # 导入win32api相关模块
import time
from PIL import Image
from lib import pyscreeze
import cv2

class Controls:

    screen = None
    form = None
    offset_left = 0
    offset_right = 0
    offset_top = 0
    offset_bottom = 0
    thread = None

    @classmethod
    def sleep(cls,times):
        if cls.thread == None:
            time.sleep(times)
        else:
            cls.thread.msleep(int(times*100))

    @classmethod
    def get_screen(cls, hwnd):
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
            "RGB",
            (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
            bmpstr,
            "raw",
            "BGRX",
            0,
            1,
        )
        # bmpfilenamename = "jiuyin.png"
        # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        # 清理内存
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        cls.screen = image

    @classmethod
    def localall(cls, path, hwnd, confidence=0.9, **kwargs):
        locat_all = []
        all_list = cls.locateAll(
            path, confidence = confidence, **kwargs
        )
        if not all_list:
            return []
        for box in all_list:
            if box is None:
                return []
            locat_all.append(cls.offset_box(box))
        return locat_all

    @classmethod
    def locate(cls, path, hwnd, contrast_ratio=0.9,offset_form=None):
        loca_box = pyscreeze.locate(
            path, cls.screen, confidence=contrast_ratio,region=offset_form)
        return cls.offset_box(loca_box)

    @classmethod
    def get_offset(cls):
        return cls.offset_left,cls.offset_top

    @classmethod
    def offset_box(cls, box):
        if box is None:
            return None
        new_left = box.left + cls.offset_left
        new_top = box.top + cls.offset_top
        box._replace(left=new_left)
        box._replace(top=new_top)
        return box

    @staticmethod
    def activate_hwnd(hwnd):
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATEAPP, 0x1, 0)
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATE, 0x2, 0)
        win32api.SendMessage(hwnd, win32con.WM_IME_SETCONTEXT, 0x1, 0xC000000F)
        win32api.SendMessage(hwnd, win32con.WM_IME_NOTIFY, 0x2, 0)

    @staticmethod
    def un_activate_hwnd(hwnd):
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATEAPP, 0, 0)
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATE, 0, 0)

    # 键盘摁下抬起
    @classmethod
    def key_post(cls,hwnd, key, sleep_time=0):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0x2E0001)
        if sleep_time > 0:
            cls.sleep(sleep_time)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0x2E0001)

    @staticmethod
    def win_mouse_click_box(hwnd, box, rexy=False, sleep_tim=0.2):
        Controls.activate_hwnd(hwnd)
        if rexy:
            x, y = Controls.get_box_xy(box)
        else:
            x = box.left
            y = box.top
        Controls.win_mouse_click(hwnd, x, y, sleep_tim)
        Controls.un_activate_hwnd(hwnd)

    # 直接发起鼠标点击，走windows窗口事件
    @classmethod
    def win_mouse_click(cls,hwnd, x, y, sleep_time=0.2):
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, point)
        cls.sleep(sleep_time)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 1, point)

    @classmethod
    def win_mouse_move(cls,hwnd, x, y, sleep_time=1):
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, point)
        cls.sleep(sleep_time)

    # 闪烁窗口
    @staticmethod
    def flash_hwnd(hwnd, type=True, flash_num=2, time=0):
        win32gui.FlashWindowEx(hwnd, type, flash_num, time)

    @staticmethod
    def get_box_xy(box):
        x = box.left + box.width/2
        y = box.top - box.height
        return int(x), int(y)

    @staticmethod
    def win_gunlun_qian(hwnd):
        for _ in range(50):
            win32api.PostMessage(hwnd, win32con.WM_MOUSEWHEEL, 0x780000, 0x0176022C)

    @classmethod
    def locateAll(cls,path,**kwargs):
        box_list = pyscreeze.locateAll(path,cls.screen,**kwargs)
        # box_list = pyautogui.locateAll(path,cls.screen,**kwargs)
        new_list = []
        box_list = list(box_list)
        box_list.sort(key = lambda x:x.left)
        last_box = None
        for box in box_list:
            if last_box == None:
                last_box = box
                new_list.append(box)
                continue
            if (box.left - last_box.left) <= 5:
                continue
            last_box = box
            new_list.append(box)
        return new_list

    @classmethod
    def get_tuanlian_box(cls,path,hwnd,confidence,region = None,**kwargs):
        target_img = pyscreeze.load_cv2(path)
        tem_img = pyscreeze.load_cv2(cls.screen)

        # 灰度图像
        target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        tem_gray = cv2.cvtColor(tem_img, cv2.COLOR_BGR2GRAY)
        if region:
            tem_gray = tem_gray[region[1]:region[1]+region[3],
                                        region[0]:region[0]+region[2]]

        #二值化
        target_ret, target_binary = cv2.threshold(target_gray, 96, 255, cv2.THRESH_BINARY_INV)
        tem_ret, tem_binary = cv2.threshold(tem_gray, 96, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow("target_binary", target_binary)
        # cv2.imshow("tem_binary", tem_binary)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(type(target_binary))
        # print(type(tem_binary))
        cv2.imwrite("im_save1.png", target_binary)
        cv2.imwrite("im_save2.png", tem_binary)

        box_list = pyscreeze.locateAll_opencv(target_binary,tem_binary,confidence=confidence,**kwargs)
        new_list = []
        box_list = list(box_list)
        box_list.sort(key = lambda x:x.left)
        last_box = None
        for box in box_list:
            if last_box == None:
                last_box = box
                new_list.append(box)
                continue
            if (box.left - last_box.left) <= 5:
                continue
            last_box = box
            new_list.append(box)
        return new_list