import pyscreeze


mubiao = "D:\demo\jiuyin_robot\Demo\img\kkkk.png"
pipei = "D:\demo\jiuyin_robot\Demo\img\\tl.png"



if __name__ == '__main__':
    box = pyscreeze.locateAll_opencv(mubiao,pipei,confidence=0.5)
    print(list(box))