from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import pyautogui
import win32con
from loguru import logger


# 状态：
stop = 0
move_to_npc = 1
# 点击npc
click_npc = 2
# 点击接镖
click_begin = 3
# 选择路线
chose_path = 4
# 选择乘车
click_mache = 5
# 拉镖状态
in_labiao = 6
# 攻击劫匪
atk_jiefei = 7
# 劫匪死亡，重新进入拉镖状态
reset_labiao = 8
# 劫匪死亡后的拉镖状态
reset_in_labiao = 9
# 拉镖结束
labiao_end = 10

# 拉镖
class LaBiao(BaseModule):
    
    is_act = False
    this_state = stop

    def __init__(self):
        logger.info("初始化拉镖模块")

    def update_hwnd(self,hwnd):
        if self.this_state == stop:
            return
        if self.this_state == move_to_npc:
            self.check_is_over_move()
        if self.this_state == click_npc:
            self.check_jiebiao()
        if self.this_state == chose_path:
            self.chose_path()
        if self.this_state == click_mache:
            self.check_chengche()
        if self.this_state == in_labiao:
            self.wait_jiefei()
        if self.this_state == atk_jiefei:
            self.check_jiefei_death()
        if self.this_state == reset_labiao:
            self.reset_labiao()
        if self.this_state == reset_in_labiao:
            self.check_labiao_end()
        if self.this_state == labiao_end:
            self.try_to_reset()

    # 检测是否移动到了拉镖npc旁边
    def check_is_over_move(self):
        pass

    # 点击接镖
    def check_jiebiao(self):
        pass

    # 选择路线
    def chose_path(self):
        pass

    # 选择乘车
    def check_chengche(self):
        pass

    # 检测是否有劫匪
    def wait_jiefei(self):
        pass

    # 检测劫匪是否死亡
    def check_jiefei_death(self):
        pass

    # 重新进入拉镖状态
    def reset_labiao(self):
        pass

    # 判断拉镖是否结束
    def check_labiao_end(self):
        pass

    # 重新拉镖 
    def try_to_reset(self):
        pass


    def module_start(self):
        self.is_act = True
        self.this_state = move_to_npc
        # 移动到npc
    
    def module_end(self):
        self.is_act = False
        self.this_state = stop
