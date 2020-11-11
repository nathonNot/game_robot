import importlib
import argparse
import os
import time
import threading
from lib.BaseModule import BaseModule
from lib.utils import init_file
import lib.global_data as gbd


if __name__ == '__main__':
    path = "GameRobot/chuanqi_web/script"
    init_file(path)
    while(True):
        for m in gbd.module_list:
            m.fram_update()
        time.sleep(1)
