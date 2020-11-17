
import win32gui, win32ui, win32con
from ctypes import windll

def set_windwos():
    hWndList = [] 
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList) 
    for hwnd in hWndList:
        # clsname = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if (title.find("九阴真经") >= 0): #调整目标窗口到坐标(600,300),大小设置为(600,600)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,800,600, win32con.SWP_SHOWWINDOW)
            # screenshot_by_hwnd(hwnd)
    #查找窗口句柄
    # win32gui.FindWindow("")