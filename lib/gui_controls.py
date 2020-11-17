import pyautogui

class Controls:

    # 路径，对比度
    @staticmethod
    def get_screen_box(path,contrast_ratio = 0.9):
        return pyautogui.locateOnScreen(path,confidence=contrast_ratio)

    @staticmethod
    def get_screen_box_all(path,contrast_ratio = 0.9):
        return pyautogui.locateAllOnScreen(path,confidence=contrast_ratio)

    # 右键单击,路径中不能有中文
    @staticmethod
    def right_click(path):
        coords = get_screen_box(path)
        if coords:
            #获取定位到的图中间点坐标
            x,y=pyautogui.center(coords)
            #右击该坐标点
            pyautogui.rightClick(x,y)
            return True
        return False

    # 左键单击,路径中不能有中文
    @staticmethod
    def left_click(path):
        coords = get_screen_box(path)
        if coords:
            print("找到"+path)
            #获取定位到的图中间点坐标
            x,y=pyautogui.center(coords)
            #右击该坐标点
            pyautogui.leftClick(x,y)
            return True
        return False