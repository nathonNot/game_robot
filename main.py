import importlib
import argparse
import os

file_name = []
path = "Demo/test_import"
for file in os.listdir(path):
    if os.path.splitext(file)[1]=='.py':
        file_name.append(file)
print(file_name)

for file in file_name:
    moudle = file.split(".")[0]
    moudle_name = "Demo.test_import." + moudle
    lib = importlib.import_module(moudle_name)
    print(lib.__dir__())
    # instance = lib.A()
    # instance.funcname()
# lib = importlib.import_module("from Demo.test_import import * ")
