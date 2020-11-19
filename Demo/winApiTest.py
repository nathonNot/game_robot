import win32api,win32gui,win32con #导入win32api相关模块
 
# windows ='111.txt' #窗口的类名
# hwnd = win32gui.FindWindow(windows,None)#通过窗口类名获取窗口句柄

# k 0x4B
# j 0x4A
# win32con.VK_LEFT 左
# VK_UP 上
# VK_RIGHT 右
# VK_DOWN 下 

if __name__ == '__main__':
    win32api.PostMessage(8915604, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)#发送F9键
    win32api.PostMessage(8915604, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
    