
import win32gui, win32ui, win32con
from ctypes import windll
from lib import global_data

def set_windwos():
    hWndList = []
    global_data.hwnd_list.clear()
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList) 
    for hwnd in hWndList:
        # clsname = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        # if "Flask" in title:
        print(hwnd,title)
        # print(title,hwnd)
        if (title.find("九阴真经") >= 0): #调整目标窗口到坐标(600,300),大小设置为(600,600)
            global_data.hwnd_list.append(hwnd)
            # screenshot_by_hwnd(hwnd)
    x,y = 0,0
    for hwnd in global_data.hwnd_list:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,800,600, win32con.SWP_SHOWWINDOW)
        if x == 0:
            x+=800
        else:
            x = 0
        if y == 0:
            y += 600
        else:
            y = 0
    #查找窗口句柄
    # win32gui.FindWindow("")