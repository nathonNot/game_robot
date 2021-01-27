import lib.global_data as gbd
from loguru import logger
from config import init_config
from model.main_windows import show_login
import traceback

def main():
    try:
        succ = init_config()  #初始化配置
        if succ is None:
            return
        logger.info("设置九阴窗口")
        import game_robot
        gbd.Exit = False
        show_login()
    except Exception as e:
        logger.error(str(e))
        msg = traceback.format_exc()
        logger.error(msg)

if __name__ == "__main__":
    main()
    input()
