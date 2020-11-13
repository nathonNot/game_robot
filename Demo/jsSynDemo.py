# 键鼠同步测试


import pynput

with pynput.mouse.Events() as event:

    for i in event:
    #迭代用法。
        if isinstance(i, pynput.mouse.Events.Move):
            #鼠标移动事件。
            print(i.x, i.y)
            #不要直接打印`i`，模块这里有问题，会报错。

        elif isinstance(i, pynput.mouse.Events.Click):
            #鼠标点击事件。
            print(i.x, i.y, i.button, i.pressed)
            #这个i.button就是上文所说的“鼠标按键”中的一个，用is语句判断即可。

        elif isinstance(i, pynput.mouse.Events.Scroll):
            #鼠标滚轮。
            print(i.x, i.y, i.dx, i.dy)


        break
    
    i = event.get(1)
    #另一种用法。
    #默认值是None。
    #这个`1`就是最长等待时间，超过这个时间没有事件，
    #就会报错。错误类型是queue模块的Empty，而非TimeoutError。