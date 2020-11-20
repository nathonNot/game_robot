import pyautogui
import win32api,win32gui,win32con #导入win32api相关模块

class Controls:

    screen = None
    form = None

    @classmethod
    def get_screen(cls):
        cls.screen = pyautogui.screenshot()

    @classmethod
    def localall(cls,path,hwnd,contrast_ratio=0.9):
        cls.get_hwnd_form(hwnd)
        return pyautogui.locateAll(path, cls.screen,region=cls.form,confidence = contrast_ratio)

    @classmethod
    def locate(cls,path,hwnd,contrast_ratio=0.9):
        cls.get_hwnd_form(hwnd)
        return pyautogui.locate(image, screenshotIm,region=cls.form)

    @classmethod
    def get_hwnd_form(cls,hwnd):
        xleft, ytop, xright, ybottom = win32gui.GetWindowRect(hwnd)
        cls.form = (xleft, ytop, (xright - xleft), (ybottom - ytop))

    @classmethod
    def screen_close(cls):
        try:
            cls.screen.fp.close()
        except AttributeError:
            # Screenshots on Windows won't have an fp since they came from
            # ImageGrab, not a file. Screenshots on Linux will have fp set
            # to None since the file has been unlinked
            pass

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
            print("找到"+path)
            # 获取定位到的图中间点坐标
            x, y = pyautogui.center(coords)
            # 右击该坐标点
            pyautogui.leftClick(x, y)
            return True
        return False

    @staticmethod
    def activate_hwnd(hwnd):
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATEAPP,0x1,0)
        win32api.SendMessage(hwnd, win32con.WM_ACTIVATE,0x2,0)
        win32api.SendMessage(hwnd, win32con.WM_IME_SETCONTEXT,0x1,0xC000000F)
        win32api.SendMessage(hwnd, win32con.WM_IME_NOTIFY,0x2,0)

    # 键盘摁下抬起
    @staticmethod
    def key_post(hwnd,key):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0x2E0001)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0x2E0001)