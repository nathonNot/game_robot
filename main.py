import importlib
import argparse
import os
import time
import threading
from lib.BaseModule import BaseModule


def init_file(path: str):
    global file_name
    global module_list
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.py':
            file_name.append(file)

    base_module_path = path.replace("/", ".")

    for file in file_name:
        moudle = file.split(".")[0]
        moudle_name = base_module_path+"." + moudle
        lib = importlib.import_module(moudle_name)
        print(lib.__dir__())
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
                    module_list.append(base)
            except Exception as identifier:
                pass
    print(module_list)


if __name__ == '__main__':
    file_name = []
    module_list = []
    path = "Demo/test_import"
    init_file(path)
    while(True):
        for m in module_list:
            m.fram_update()
        time.sleep(1)
