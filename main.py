import lib.global_data as gbd
from loguru import logger
from lib.thread_class import MainRefresh
from config import init_config
from model.main_windows import show_login


def main():
    succ = init_config()  #初始化配置
    if succ is None:
        return
    logger.info("设置九阴窗口")
    import game_robot
    gbd.Exit = False
    show_login()


if __name__ == "__main__":
    main()
    input()
