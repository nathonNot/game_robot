import importlib
import argparse
import os
import lib.global_data as gbd
import datetime
import lib.windows_con as win_con
import lib
import json
from loguru import logger
import win32con
from lib.thread_class import Hotkey,MainRefresh
from config import init_config

threads = []

def start_thread():
    global threads
    main_thread = MainRefresh()
    main_thread.start()
    threads.append(main_thread)
    Hk = Hotkey()
    Hk.start()
    threads.append(Hk)

def main():

    succ = init_config()  #初始化配置
    if succ is None:
        return
    logger.info("设置九阴窗口")
    import game_robot
    gbd.Exit = True
    start_thread()

    global threads
    for t in threads:
        t.join()



if __name__ == "__main__":
    main()
    input()
