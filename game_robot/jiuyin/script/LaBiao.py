from logging import LogRecord
from lib.BaseModule import BaseModule
from lib.gui_controls import Controls
import win32con
from loguru import logger
from game_robot.jiuyin import utils as jiuyin_game
import time

# 状态：
stop = -1
start = 0
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
    this_hwnd = 0
    next_move = False
    
    def __init__(self):
        logger.info("初始化拉镖模块")

    def update_hwnd(self,hwnd):
        if self.this_state == stop:
            return
        self.this_hwnd = hwnd
        # 判断拉镖图标是否存在
        lb_icon = Controls.locate("image\lb_icon.png",self.this_hwnd)
        if not lb_icon and self.this_state == in_labiao:
            self.this_state = labiao_end
        elif self.this_state == start:
            self.reset_labiao()
        elif self.this_state == move_to_npc:
            self.check_is_over_move()
        elif self.this_state == click_npc:
            self.check_jiebiao()
        elif self.this_state == chose_path:
            self.chose_path()
        elif self.this_state == click_mache:
            self.check_chengche()
        elif self.this_state == in_labiao:
            self.wait_jiefei()
        elif self.this_state == atk_jiefei:
            self.check_jiefei_death()
        elif self.this_state == reset_labiao:
            self.reset_labiao()
        elif self.this_state == reset_in_labiao:
            self.check_labiao_end()
        elif self.this_state == labiao_end:
            self.reset_labiao()
            self.try_to_reset()

    # 检测是否移动到了拉镖npc旁边
    def check_is_over_move(self):
        # Controls.activate_hwnd(self.this_hwnd)
        # Controls.win_mouse_click(self.this_hwnd, 697, 93)
        jiebiao = Controls.locate("image\lb_jiebiao.png",self.this_hwnd,0.8)
        if jiebiao:
            x = jiebiao.left
            y = jiebiao.top - jiebiao.height/2
            Controls.win_mouse_click(self.this_hwnd,int(x),int(y))
            logger.debug("移动到接镖npc完成")
            time.sleep(2)
            self.this_state = chose_path
        else:
            self.next_move = True

    # 点击接镖
    def check_jiebiao(self):
        pass

    # 选择路线
    def chose_path(self):
        xiaobiaoche = Controls.locate("image\lb_xiaobiaoche.png",self.this_hwnd,0.8)
        if xiaobiaoche:
            Controls.activate_hwnd(self.this_hwnd)
            Controls.win_mouse_click(self.this_hwnd,410,300)
            self.this_state = click_mache
        else:
            self.this_state = move_to_npc

    # 选择乘车
    def check_chengche(self):
        jiache = Controls.locate("image\lb_jiache.png",self.this_hwnd)
        if jiache:
            Controls.activate_hwnd(self.this_hwnd)
            Controls.key_post(self.this_hwnd,0x57)
            Controls.win_mouse_click_box(self.this_hwnd,jiache,True)
            self.this_state = in_labiao
            return 
        jiebiao_ok = Controls.locate("image\lb_queding.png",self.this_hwnd)
        if jiebiao_ok:
            Controls.activate_hwnd(self.this_hwnd)
            Controls.win_mouse_click_box(self.this_hwnd,jiebiao_ok,True)
            return
        jiebiao = Controls.locate("image\lb_jiebiaot.png",self.this_hwnd,0.5)
        if jiebiao:
            Controls.activate_hwnd(self.this_hwnd)
            Controls.win_mouse_click_box(self.this_hwnd,jiebiao,True)
            return

    # 检测是否有劫匪
    def wait_jiefei(self):
        key_list = [49,50,51,52]
        Controls.activate_hwnd(self.this_hwnd)
        for key in key_list:
            Controls.key_post(self.this_hwnd,key)

    # 检测劫匪是否死亡
    def check_jiefei_death(self):
        pass

    # 重新进入拉镖状态
    def reset_labiao(self):
        Controls.activate_hwnd(self.this_hwnd)
        lb_map_box = Controls.locate("D:\project\python\jiuyin_robot\image\lb_chengdu.png",self.this_hwnd,0.8)
        if lb_map_box:
            Controls.key_post(self.this_hwnd,0x57)
            Controls.win_mouse_click_box(self.this_hwnd,lb_map_box,True)
            time.sleep(0.1)
            Controls.win_mouse_click_box(self.this_hwnd,lb_map_box,True)
            Controls.key_post(self.this_hwnd,0x57)
            return
        map_box = Controls.locate("image\map_biaoqian.png",self.this_hwnd,0.8)
        if map_box:
            Controls.key_post(self.this_hwnd,0x57)
            Controls.win_mouse_click_box(self.this_hwnd,map_box,True)
        # 移动到npc
        x,y = jiuyin_game.get_xy(722,517)
        # 打开地图
        # 视角距离滑动拉到最近
        Controls.win_gunlun_qian(self.this_hwnd)
        Controls.key_post(self.this_hwnd,0x4D)
        jiuyin_game.move_to_pos(self.this_hwnd,x,y)
        # self.this_state = move_to_npc
        time.sleep(2)

    # 判断拉镖是否结束
    def check_labiao_end(self):
        pass

    # 重新拉镖 
    def try_to_reset(self):
        pass

    def module_end(self):
        self.is_act = False
        self.this_state = stop

    def stop(self):
        self.this_state = stop
    
    def start(self):
        self.this_state = start