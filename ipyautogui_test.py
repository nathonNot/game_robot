import pyautogui
import cv2

# 右键单击,路径中不能有中文
def right_click(path):
    coords = pyautogui.locateOnScreen(path)
    if coords:
        #获取定位到的图中间点坐标
        x,y=pyautogui.center(coords)
        #右击该坐标点
        pyautogui.rightClick(x,y)
    return False


if __name__ == '__main__':
    right_click("image\\vs_code.png")
    