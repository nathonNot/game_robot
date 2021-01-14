from qt_ui.Ui_main import Ui_main
from lib.ui_lib import BaseForm
from lib import global_data as gbd
import webbrowser
from lib.thread_class import WebSocketThread, MainRefresh
from lib.utils import start_thread, thread_stop
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,pyqtSignal,QObject
from lib import socket_msg
from lib.web_socket import WebSocketClient
from lib.windows_con import get_jiuyin_hwnd
from lib.gui_controls import Controls
from lib.utils import win_key_dc
from lib.thread_class import KeyRangeThread
from model.form_caiji import CaiJiForm

class MainForm(Ui_main, BaseForm,QObject):

    set_data_signal = pyqtSignal(list)
    ref_data = pyqtSignal()
    ref_val = None

    def setupUi(self, LoginForm):
        super().setupUi(LoginForm)
        self.le_range_num.setValidator(QIntValidator(0, 65535))
        self.le_range_sleep_time.setValidator(QIntValidator(0, 65535))
        self.refresh_main_win_combox()
        self.refresh_key_range_combox()
        self.set_caiji = CaiJiForm()
        self.set_caiji.init()

    def show_ui(self):
        self.lb_user_name.setText(gbd.user_data.user_name)
        self.lb_key_list.setText("")
        self.bt_chongzhi.setVisible(False)
        self.bt_ws_con.setVisible(False)
        # self.cb_labiao.setVisible(False)
        self.widget.show()
        self.lb_vip_end_time.setText(gbd.user_data.vip_end_time)

    def init_callback(self):
        self.bt_chongzhi.clicked.connect(self.open_chongzhi)
        self.bt_ws_con.clicked.connect(self.on_bt_ws_con_clicked)

        self.cb_tuanlian.clicked.connect(self.on_cb_tuanlian_clicked)
        self.cb_neigong.clicked.connect(self.on_cb_neigong_clicked)
        self.cb_shashou.clicked.connect(self.on_cb_shashou_clicked)
        self.cb_tanwei.clicked.connect(self.on_cb_tanwei_clicked)
        self.bt_start_up.clicked.connect(self.on_bt_start_up_clicked)
        self.bt_start2.clicked.connect(self.on_bt_start_up_clicked)
        self.cb_main_win.clicked.connect(self.on_cb_main_win_clicked)
        self.cb_lianan.clicked.connect(self.on_cb_lianan_clicked)
        self.set_data_signal.connect(self.set_data)
        self.cbb_main_win.currentIndexChanged.connect(self.on_cbb_main_win_index_changed)
        self.cbb_target_hwnd.currentIndexChanged.connect(self.on_cbb_target_ndex_changed)
        self.bt_add_key.clicked.connect(self.on_bt_add_key_clicked)
        self.bt_clear_key_list.clicked.connect(self.on_bt_clear_key_list_clicked)
        self.bt_start_range_key.clicked.connect(self.on_bt_start_range_key_clicked)
        self.cb_labiao.clicked.connect(self.on_cb_labiao_clicked)
        self.bt_add_hwnd.clicked.connect(self.on_bt_add_hwnd_check)
        self.bt_clear_main_hwnd.clicked.connect(self.on_clear_bt_hwnd_check)
        # self.cbb_main_win.clicked.connect(self.refresh_main_win_combox)
        # self.cbb_target_hwnd.clicked.connect(self.refresh_main_win_combox)

    def show_caiji(self):
        self.set_caiji.show_ui()

    def open_chongzhi(self):
        url = "www.baidu.com"
        webbrowser.open(url)

    def on_bt_start_range_key_clicked(self):
        if (self.bt_start_range_key.text == "正在循环按键"):
            return
        hwnd = self.cbb_target_hwnd.currentText()
        run_times = self.le_range_num.text()
        try:
            hwnd = int(hwnd)
            run_times = int(run_times)
        except Exception as identifier:
            self.lb_log.setText(str(identifier))
            return
        sleep_times = self.le_range_sleep_time.text()
        q_thread = KeyRangeThread(hwnd,run_times,int(sleep_times))
        q_thread.thread_done.connect(self.thread_key_range_done)
        start_thread(q_thread,False)
        self.bt_start_range_key.setText("正在循环按键")
        self.bt_start_range_key.setEnabled(False)

    def on_bt_add_key_clicked(self):
        key = self.cbb_key.currentText()
        gbd.key_range_list.append(win_key_dc[key])
        old_text = self.lb_key_list.text()
        if old_text != "":
            old_text += ","
        old_text += key
        self.lb_key_list.setText(old_text)

    def on_bt_clear_key_list_clicked(self):
        gbd.key_range_list.clear()
        self.lb_key_list.setText("")

    def on_cb_neigong_clicked(self):
        gbd.module_dc["内功"].is_act = self.cb_neigong.isChecked()

    def on_cb_tuanlian_clicked(self):
        gbd.module_dc["团练"].is_act = self.cb_tuanlian.isChecked()
    
    def on_cb_shashou_clicked(self):
        gbd.module_dc["杀手"].is_act = self.cb_shashou.isChecked()
    
    def on_cb_tanwei_clicked(self):
        gbd.module_dc["摊位"].is_act = self.cb_tanwei.isChecked()
    
    def on_cb_lianan_clicked(self):
        gbd.module_dc["连按"].is_act = self.cb_lianan.isChecked()

    def on_cb_labiao_clicked(self):
        gbd.module_dc["拉镖"].is_act = self.cb_labiao.isChecked()
        if self.cb_labiao.isChecked():
            gbd.module_dc["拉镖"].start()
        else:
            gbd.module_dc["拉镖"].stop()

    def on_bt_start_up_clicked(self):
        if gbd.Exit:
            gbd.Exit = False
            thread_stop(MainRefresh)
            self.bt_start_up.setText("启动")
            self.bt_start2.setText("启动")
        else:
            self.bt_start_up.setText("停止")
            self.bt_start2.setText("停止")
            thread_stop(MainRefresh)
            gbd.Exit = True
            start_thread(MainRefresh)

    def on_bt_ws_con_clicked(self):
        bt_text = self.bt_ws_con.text()
        if bt_text == "连接到服务器":
            start_thread(WebSocketThread)
            self.bt_ws_con.setText("断开服务器连接")
        else:
            thread_stop(WebSocketThread)
            self.bt_ws_con.setText("连接到服务器")
    
    def set_data(self,data):
        self.ref_val = data

    def on_ref_data(self):
        if self.ref_val == None:
            return
        self.tw_citan_data.clearContents()
        for task in self.ref_val:
            task_data = {
                "id" : task["task_id"],
                "acc":task["account_number"],
                "pas":task["account_password"],
                "server1":task["server1"],
                "server2":task["server2"],
                "update_time":task["task_change_time"],
                "start_time":task["task_start_time"],
                "status":task["task_status"]
            }
            self.install_tb_row(**task_data)
        self.ref_val = None
    
    # 刷新主游戏下拉框
    def refresh_main_win_combox(self):
        if len(gbd.hwnd_list) < 1:
            gbd.hwnd_list = get_jiuyin_hwnd()
        self.cbb_main_win.addItems([str(i) for i in gbd.hwnd_list])
        self.cbb_target_hwnd.addItems([str(i) for i in gbd.hwnd_list])

    def on_cb_main_win_clicked(self):
        if self.cb_main_win.isChecked():
            gbd.main_window_no_flush = True
        else:
            gbd.main_window_no_flush = False
    
    def on_cbb_main_win_index_changed(self):
        hwnd = self.cbb_main_win.currentText()
        Controls.flash_hwnd(int(hwnd))
    
    def on_cbb_target_ndex_changed(self):
        hwnd = self.cbb_target_hwnd.currentText()
        Controls.flash_hwnd(int(hwnd))

    # 刷新按键循环下拉框
    def refresh_key_range_combox(self):
        key_list = list(win_key_dc.keys())
        self.cbb_key.addItems(key_list)

    def thread_key_range_done(self):
        self.bt_start_range_key.setText("开始循环")
        self.bt_start_range_key.setEnabled(True)

    def on_bt_add_hwnd_check(self):
        hwnd = self.cbb_main_win.currentText()
        gbd.main_window_hwnd.append(int(hwnd))
        gbd.main_window_hwnd = list(set(gbd.main_window_hwnd))
        new_text = ",".join([str(i) for i in gbd.main_window_hwnd])
        self.lb_hwnd_list.setText(new_text)
    
    def on_clear_bt_hwnd_check(self):
        self.lb_hwnd_list.setText("")
        gbd.main_window_hwnd.clear()