import importlib
import os
from lib.BaseModule import BaseModule
import lib.global_data as gbd
from lib.thread_class import MainRefresh
from loguru import logger

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


def start_thread(thread_obj):
    class_name = thread_obj.class_name()
    if class_name in gbd.threads:
        return
    thread = thread_obj()
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
        del gbd.threads[class_name]