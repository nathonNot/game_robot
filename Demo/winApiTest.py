import win32api,win32gui,win32con #导入win32api相关模块
import time

def get_hwnd():
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList) 
    for hwnd in hWndList:
        title = win32gui.GetWindowText(hwnd)
        if (title.find("九阴真经  江湖") >= 0) or (title.find("九阴真经  武侠") >= 0): #调整目标窗口到坐标(600,300),大小设置为(600,600)
            print(hwnd,title)
# k 0x4B
# j 0x4A
# win32con.VK_LEFT 左
# VK_UP 上
# VK_RIGHT 右
# VK_DOWN 下 
# win32api.PostMessage(8915604, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)#发送F9键
# win32api.PostMessage(8915604, win32con.WM_KEYUP, win32con.VK_LEFT, 0)

def test_done1():
    win32api.PostMessage(200352, win32con.WM_LBUTTONDOWN, 1, 0x003002F3)
    time.sleep(1)
    win32api.PostMessage(200352, win32con.WM_LBUTTONUP, 1, 0x003002F3)

def mouse_click(point):
    win32api.PostMessage(200352, win32con.WM_LBUTTONDOWN, 1, point)
    time.sleep(1)
    win32api.PostMessage(200352, win32con.WM_LBUTTONUP, 1, point)

if __name__ == '__main__':
    print(get_hwnd())
    # for x in (600,650):
    point = win32api.MAKELONG(686, 81) 
    win32api.PostMessage(200352, win32con.WM_MOUSEMOVE, 0, point)
    mouse_click(point)
        # win32api.PostMessage(200352, win32con.WM_NCHITTEST, 0, point)
        # time.sleep(1)
        # win32api.PostMessage(200352,win32con.WM_SETCURSOR,0x00030EA0,0x02000001)