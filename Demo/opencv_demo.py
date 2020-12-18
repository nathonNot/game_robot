import pyscreeze


mubiao = "D:\demo\jiuyin_robot\Demo\img\kkkk.png"
pipei = "D:\demo\jiuyin_robot\Demo\img\\tl.png"


def get_box():
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


if __name__ == '__main__':
    get_box()