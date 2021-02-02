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

    def __init__(self,is_run):
        self.is_run = is_run

    @staticmethod
    def get_self(hwnd):
        from lib import global_data as gbd
        return gbd.hwnd_work_dc[hwnd]

    @classmethod
    def sleep(cls,times):
        if cls.thread == None:
            time.sleep(times)
        else:
            cls.thread.msleep(int(times*100))

    @staticmethod
    def get_screen(hwnd):
        loc = Controls.get_self(hwnd)
        if not loc.is_run:
            return
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        loc.offset_left = left
        loc.offset_right = right
        loc.offset_bottom = bottom
        loc.offset_top = top
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
        loc.screen = image

    @staticmethod
    def localall(path, hwnd, confidence=0.9, **kwargs):
        loc = Controls.get_self(hwnd)
        if not loc.is_run:
            return
        locat_all = []
        all_list = loc.locateAll(
            path, confidence = confidence, **kwargs
        )
        if not all_list:
            return []
        for box in all_list:
            if box is None:
                return []
            locat_all.append(loc.offset_box(box))
        return locat_all

    @staticmethod
    def locate(path, hwnd, contrast_ratio=0.9,offset_form=None):
        loc = Controls.get_self(hwnd)
        if not loc.is_run:
            return
        loca_box = pyscreeze.locate(
            path, loc.screen, confidence=contrast_ratio,region=offset_form)
        return loc.offset_box(loca_box)

    @staticmethod
    def get_offset(hwnd):
        loc = Controls.get_self(hwnd)
        return loc.offset_left,loc.offset_top

    def offset_box(self, box):
        if not self.is_run:
            return
        if box is None:
            return None
        new_left = box.left + self.offset_left
        new_top = box.top + self.offset_top
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

    @classmethod
    def key_post(cls,hwnd, key, sleep_time=0):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0x2E0001)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0x2E0001)
        if sleep_time > 0:
            cls.sleep(sleep_time)

    @staticmethod
    def win_mouse_click_box(hwnd, box, rexy=False, sleep_tim=0.2):
        loc = Controls.get_self(hwnd)
        if not loc.is_run:
            return
        loc.activate_hwnd(hwnd)
        if rexy:
            x, y = loc.get_box_xy(box)
        else:
            x = box.left
            y = box.top
        loc.win_mouse_click(hwnd, x, y, sleep_tim)
        loc.un_activate_hwnd(hwnd)

    # 直接发起鼠标点击，走windows窗口事件
    @staticmethod
    def win_mouse_click(hwnd, x, y, sleep_time=0.2):
        loc = Controls.get_self(hwnd)
        if not loc.is_run:
            return
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, point)
        loc.sleep(sleep_time)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 1, point)

    # 直接发起鼠标点击，走windows窗口事件
    @staticmethod
    def win_mouse_right_click(hwnd, x, y, sleep_time=0.2):
        loc = Controls.get_self(hwnd)
        if not loc.is_run:
            return
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 1, point)
        loc.sleep(sleep_time)
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, 1, point)

    @staticmethod
    def win_mouse_move(hwnd, x, y, sleep_time=1):
        loc = Controls.get_self(hwnd)
        if not loc.is_run:
            return
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, point)
        loc.sleep(sleep_time)

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
            win32api.PostMessage(hwnd, win32con.WM_MOUSELAST, 0xFF880000, 0x014501DC)
        # for _ in range(10):
        #     win32api.PostMessage(hwnd, win32con.WM_MOUSEWHEEL, 0x780000, 0x0176022C)

    def locateAll(self,path,**kwargs):
        if not self.is_run:
            return
        box_list = pyscreeze.locateAll(path,self.screen,**kwargs)
        # box_list = pyautogui.locateAll(path,self.screen,**kwargs)
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

    # def get_tuanlian_box(self,path,hwnd,confidence,region = None,**kwargs):
    #     if self.is_run:
    #         return
    #     target_img = pyscreeze.load_cv2(path)
    #     tem_img = pyscreeze.load_cv2(self.screen)

    #     # 灰度图像
    #     target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    #     tem_gray = cv2.cvtColor(tem_img, cv2.COLOR_BGR2GRAY)
    #     if region:
    #         tem_gray = tem_gray[region[1]:region[1]+region[3],
    #                                     region[0]:region[0]+region[2]]

    #     #二值化
    #     target_ret, target_binary = cv2.threshold(target_gray, 96, 255, cv2.THRESH_BINARY_INV)
    #     tem_ret, tem_binary = cv2.threshold(tem_gray, 96, 255, cv2.THRESH_BINARY_INV)
    #     # cv2.imshow("target_binary", target_binary)
    #     # cv2.imshow("tem_binary", tem_binary)
    #     # cv2.waitKey(0)
    #     # cv2.destroyAllWindows()
    #     # print(type(target_binary))
    #     # print(type(tem_binary))
    #     cv2.imwrite("im_save1.png", target_binary)
    #     cv2.imwrite("im_save2.png", tem_binary)

    #     box_list = pyscreeze.locateAll_opencv(target_binary,tem_binary,confidence=confidence,**kwargs)
    #     new_list = []
    #     box_list = list(box_list)
    #     box_list.sort(key = lambda x:x.left)
    #     last_box = None
    #     for box in box_list:
    #         if last_box == None:
    #             last_box = box
    #             new_list.append(box)
    #             continue
    #         if (box.left - last_box.left) <= 5:
    #             continue
    #         last_box = box
    #         new_list.append(box)
    #     return new_list