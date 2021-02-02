
import win32gui
import win32con
import win32api
from ctypes import windll
from lib import global_data as gbd

def set_windwos():
    base_config = gbd.config_dc["base"]
    jiuyin_hwnd = get_jiuyin_hwnd()
    if jiuyin_hwnd != gbd.hwnd_list:
        # 设置qt窗口，刷新数据
        gbd.hwnd_list = jiuyin_hwnd
        gbd.MainWindow.main_widget.ref_data.connect(gbd.MainWindow.main_widget.refresh_main_win_combox)
        gbd.MainWindow.main_widget.ref_data.emit()
        gbd.MainWindow.main_widget.ref_data.disconnect(gbd.MainWindow.main_widget.on_ref_data)
    x, y = 0, 0
    for index,hwnd in enumerate(gbd.hwnd_list):
        # 主游戏窗口不做处理
        if gbd.main_window_no_flush:
            if hwnd in gbd.main_window_hwnd:
                if gbd.user_data.is_vip():
                    continue
        # win32gui.SetWindowPos(hwnd, win32con.HWND_TOP,
        #                       x, y, 800, 600, win32con.SWP_SHOWWINDOW)
        win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM,
                              index*base_config["resolving_w"], 0, base_config["resolving_w"], base_config["resolving_h"], win32con.SWP_NOMOVE)
    # 查找窗口句柄
    # win32gui.FindWindow("")

def get_jiuyin_hwnd():
    hWndList = []
    jiuyin_hwnd = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for hwnd in hWndList:
            title = win32gui.GetWindowText(hwnd)
            # 调整目标窗口到坐标(600,300),大小设置为(600,600)
            if (title.find("九阴真经  江湖") >= 0) or (title.find("九阴真经  武侠") >= 0):
                jiuyin_hwnd.append(hwnd)
                # screenshot_by_hwnd(hwnd)
                _, win_type, _, _, _ = win32gui.GetWindowPlacement(hwnd)
                if win_type == 2:
                    win32api.MessageBox(0, "请勿将游戏窗口最小化", "重置窗口",win32con.MB_OK)
    jiuyin_hwnd.sort()
    return jiuyin_hwnd