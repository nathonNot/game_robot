from lib.func_wrap import frame_rate

class Base:
    
    def __init__(self):
        self.b = B()

    def fram_update(self):
        """
        docstring
        """
        self.b.funcname()

class B:

    def __init__(self):
        print("init b")

    def funcname(self):
        """
        docstring
        """
        print("class b")
        return 0