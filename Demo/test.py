import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2
import numpy

def main():
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

# 根据窗口句柄截图
def screenshot_by_hwnd(hWnd:int):
    #获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)

    #如果要截图到打印设备：
    ###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
    result = windll.user32.PrintWindow(hWnd,saveDC.GetSafeHdc(),0)
    print(result) #PrintWindow成功则输出1
    saveBitMap.SaveBitmapFile(saveDC,"img_Winapi.jpg")


if __name__ == '__main__':
    main()
    