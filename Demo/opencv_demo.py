import pyscreeze
import cv2
import numpy as np

def get_box():
    mubiao = "D:\demo\jiuyin_robot\Demo\img\kkkk.png"
    pipei = "D:\demo\jiuyin_robot\Demo\img\\tl.png"
    box_list = pyscreeze.locateAll_opencv(mubiao,pipei,confidence=0.5)
    new_list = []
    box_list = list(box_list)
    box_list.sort(key = lambda x:x.left)
    last_box = None
    for box in box_list:
        if last_box == None:
            last_box = box
            new_list.append(box)
            continue
        if (box.left - last_box.left) <= 5:
            continue
        last_box = box
        new_list.append(box)
    print(new_list)

def tuanlian_test():
    img = "D:\demo\jiuyin_robot\Demo\img\im_save.png"
    img = cv2.imread(img)
    # 灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #二值化
    ret, binary = cv2.threshold(gray, 96, 255, cv2.THRESH_BINARY_INV)
    #箭头轮廓
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    cv2.drawContours(img,contours,-1,(0,0,255),3)  
    cv2.imshow("img2", img)

    cv2.imshow("img", binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result = []
    if len(contours) > 10 :
        return result
    for i in range(len(contours)):
        cnt = contours[i-1]

        # cv2.drawContours(img,cnt,-1,(0,0,255),1) 
        # cv2.imshow("img", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        #最小外接矩信息
        rect = cv2.minAreaRect(cnt)
        # 获得矩形的中心点，并整数化
        boxCenter = np.int0(rect[0])
        bx = boxCenter[0]
        by = boxCenter[1]

        M = cv2.moments(cnt)
        if M['m00'] != 0:
            x ,y = M['m10'] / M['m00'], M['m01'] / M['m00']
            p = np.int0((x,y))

            px = p[0]
            py = p[1]
            # 获得x坐标差
            sx =  bx -px
            # 获得y 坐标差  
            sy =  by - py

            direction = ''
            if abs(sx) > abs(sy) :
                # x轴坐标差 大于 y轴坐标差 锁定为 左右方向
                if sx > 0 :
                    #盒子x轴大，说明箭头向左
                    direction = 'LEFT'

                else:
                    direction = 'RIGHT'
            else:
                # 这里有个问题，Y轴的坐标比较，与实际结果相反,上下方向的箭头的重心，和箭头方向是相反的，即向下的箭头，重心反而在矩形的上放
                if sy > 0:
                    direction = 'UP'
                else:
                    direction = 'DOWN'
            result.append((direction,px))
    print(result)

def tuanlian_test2(tem_path,target_path):
    target_img = cv2.imread(target_path)
    tem_img = cv2.imread(tem_path)

    # 灰度图像
    target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    tem_gray = cv2.cvtColor(tem_img, cv2.COLOR_BGR2GRAY)

    #二值化
    target_ret, target_binary = cv2.threshold(target_gray, 96, 255, cv2.THRESH_BINARY_INV)
    tem_ret, tem_binary = cv2.threshold(tem_gray, 96, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow("target_binary", target_binary)
    # cv2.imshow("tem_binary", tem_binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(type(target_binary))
    # print(type(tem_binary))

    box_list = pyscreeze.locateAll_opencv(target_binary,tem_binary)
    box_list = list(box_list)
    print(box_list)

if __name__ == '__main__':
    # tuanlian_test()
    tem_path = "D:\demo\jiuyin_robot\Demo\img\im_save.png"
    tar_path = "D:\demo\jiuyin_robot\Demo\img\\tl_down.png"
    tuanlian_test2(tem_path,tar_path)