import importlib
import os
from lib.BaseModule import BaseModule
import lib.global_data as gbd
from lib.thread_class import MainRefresh
from loguru import logger
import win32con

def init_file(path: str):
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.py':
            gbd.file_name.append(file)

    base_module_path = path.replace("/", ".")

    for file in gbd.file_name:
        moudle = file.split(".")[0]
        moudle_name = base_module_path+"." + moudle
        lib = importlib.import_module(moudle_name)
        # print(lib.__dir__())
        for d in lib.__dir__():
            if "__" in d:
                continue
            o = getattr(lib, d)
            if isinstance(o, str) or o is None:
                continue
            try:
                if issubclass(o, BaseModule) and o != type(BaseModule):
                    if o.__module__ == "lib.BaseModule":
                        continue
                    base = o()
                    gbd.module_dc[o.__module__] = base
            except Exception as identifier:
                pass
    print(gbd.module_dc)


def start_thread(thread_obj,init=True):
    class_name = thread_obj.class_name()
    if class_name in gbd.threads:
        if not gbd.threads[class_name].isFinished():
            return
        del gbd.threads[class_name]
    if init:
        thread = thread_obj()
    else:
        thread = thread_obj
    thread.start()
    gbd.threads[class_name] = thread
    # Hk = Hotkey()
    # Hk.start()
    # gbd.threads.append(Hk)
    # for t in gbd.threads:
    #     t.join()

def thread_stop(thread_obj):
    class_name = thread_obj.class_name()
    if class_name in gbd.threads:
        gbd.threads[class_name].stop()
        gbd.threads[class_name].wait()
        del gbd.threads[class_name]

win_key_dc = {
    "Backspace":win32con.VK_BACK,
    "TAB":win32con.VK_TAB,
    "Enter":win32con.VK_RETURN,
    "Shift":win32con.VK_SHIFT,
    "Ctrl":win32con.VK_CONTROL,
    "Alt":win32con.VK_MENU,
    "F1":win32con.VK_F1,
    "F2":win32con.VK_F2,
    "F3":win32con.VK_F3,
    "F4":win32con.VK_F4,
    "F5":win32con.VK_F5,
    "上":win32con.VK_UP,
    "左":win32con.VK_LEFT,
    "下":win32con.VK_DOWN,
    "右":win32con.VK_RIGHT,
    "0":48,
    "1":49,
    "2":50,
    "3":51,
    "4":52,
    "5":53,
    "6":54,
    "7":55,
    "8":56,
    "9":57,
    "j":74,
    "k":75,
    "n":78,
    "c":67,
    "d":68,
    "i":73,
    "l":76,
    "o":79,
    "p":80,
    "s":83,
    "a":65,
    "x":88,
}

win_key_iparam_dc = {
    "j":0xC0240001,
    "k":0xC0250001,
    "l":0xC0260001
}