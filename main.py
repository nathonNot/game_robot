import importlib
import argparse
import os
import time
import threading
from lib.BaseModule import BaseModule

file_name = []
path = "Demo/test_import"
for file in os.listdir(path):
    if os.path.splitext(file)[1]=='.py':
        file_name.append(file)
print(file_name)

module_list = []

for file in file_name:
    moudle = file.split(".")[0]
    moudle_name = "Demo.test_import." + moudle
    lib = importlib.import_module(moudle_name)
    print(lib.__dir__())
    for d in lib.__dir__():
        if "__" in d:
            continue
        o = getattr(lib,d)
        if isinstance(o,str) or o is None:
            continue
        try:
            if issubclass(o,BaseModule) and o != type(BaseModule):
                if o.__module__ == "lib.BaseModule":
                    continue
                base = o()
                module_list.append(base)
        except Exception as identifier:
            pass
        
    # if ("BaseModule" in lib.__dir__()):

print(module_list)

while(True):
    for m in module_list:
        m.fram_update()
    time.sleep(1)