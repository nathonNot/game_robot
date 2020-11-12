from lib.BaseModule import BaseModule

class A(BaseModule):

    def __init__(self):
        print("init")

    def fram_update(self):
        print("帧频刷新")
        return 0