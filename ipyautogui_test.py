import pyautogui
import cv2

def left_click(path): #左键点击
    left_click1 = pyautogui.locateOnScreen(path)
    print('left_click1::', left_click1)  # 返回屏幕所在位置
    if left_click1:
        url_x, url_y = pyautogui.center(left_click1)
        pyautogui.leftClick(url_x, url_y)
        return True
    return False


if __name__ == '__main__':
    left_click(r"image\\此电脑.png")
    