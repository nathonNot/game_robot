import win32
import win32gui
import win32con

def main():
    hWndList = [] 
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList) 
    for hwnd in hWndList:
        # clsname = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if (title.find("111") >= 0): #调整目标窗口到坐标(600,300),大小设置为(600,600)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600,300,600,600, win32con.SWP_SHOWWINDOW)
    #查找窗口句柄
    # win32gui.FindWindow("")



if __name__ == '__main__':
    main()
    