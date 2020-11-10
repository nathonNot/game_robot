from functools import wraps
import Demo.Global as gl

def frame_rate(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("添加帧频函数")
        gl.frame_rate_ls.append(a_func)
    return wrapTheFunction