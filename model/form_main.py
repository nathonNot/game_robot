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

    def show_ui(self):
        self.lb_user_name.setText(gbd.user_data.user_name)
        self.lb_key_list.setText("")
        self.bt_chongzhi.setVisible(False)
        self.bt_ws_con.setVisible(False)
        # self.cb_labiao.setVisible(False)
        self.widget.show()

    def init_callback(self):
        self.bt_chongzhi.clicked.connect(self.open_chongzhi)
        self.bt_ws_con.clicked.connect(self.on_bt_ws_con_clicked)

        self.cb_tuanlian.clicked.connect(self.on_cb_tuanlian_clicked)
        self.cb_neigong.clicked.connect(self.on_cb_neigong_clicked)
        self.cb_shashou.clicked.connect(self.on_cb_shashou_clicked)
        self.cb_tanwei.clicked.connect(self.on_cb_tanwei_clicked)
        self.bt_start_up.clicked.connect(self.on_bt_start_up_clicked)
        self.bt_creat_task.clicked.connect(self.on_bt_creat_task_clicked)
        self.bt_task_up.clicked.connect(self.on_bt_task_up_clicked)
        self.bt_del_task.clicked.connect(self.on_del_task_clicked)
        self.cb_main_win.clicked.connect(self.on_cb_main_win_clicked)
        self.cb_lianan.clicked.connect(self.on_cb_lianan_clicked)
        self.set_data_signal.connect(self.set_data)
        self.cbb_main_win.currentIndexChanged.connect(self.on_cbb_main_win_index_changed)
        self.bt_add_key.clicked.connect(self.on_bt_add_key_clicked)
        self.bt_clear_key_list.clicked.connect(self.on_bt_clear_key_list_clicked)
        self.bt_start_range_key.clicked.connect(self.on_bt_start_range_key_clicked)
        self.cb_labiao.clicked.connect(self.on_cb_labiao_clicked)

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
        else:
            self.bt_start_up.setText("停止")
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

    def on_bt_creat_task_clicked(self):
        self.install_tb_row(0,"000000","000000","江湖七区","醉江湖","",-1,0)

    def install_tb_row(self,id,acc,pas,server1,server2,update_time,start_time,status):
        row_count = self.tw_citan_data.rowCount()
        self.tw_citan_data.insertRow(row_count)  # 插入到第一行
        # id
        item_id = QTableWidgetItem(str(id))
        self.tw_citan_data.setItem(row_count, 0, item_id)
        item_id.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item_acc = QTableWidgetItem(str(acc))
        self.tw_citan_data.setItem(row_count, 1, item_acc)
        item_acc_pas = QTableWidgetItem(pas)
        self.tw_citan_data.setItem(row_count, 2, item_acc_pas)
        item_acc_server1 = QTableWidgetItem(server1)
        self.tw_citan_data.setItem(row_count, 3, item_acc_server1)
        item_acc_server2 = QTableWidgetItem(server2)
        self.tw_citan_data.setItem(row_count, 4, item_acc_server2)
        item_update_time = QTableWidgetItem(update_time)
        self.tw_citan_data.setItem(row_count, 5, item_update_time)
        item_update_time.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        # 定时任务时间
        start_time_combox = QComboBox()
        if int(start_time == -1):
            start_time_text = "立刻"
        start_time_text = str(0)
        start_time_combox.addItem("立刻")
        start_time_combox.addItems([str(i) for i in range(0,24)])
        start_time_combox.setCurrentText(start_time_text)
        self.tw_citan_data.setCellWidget(row_count, 6, start_time_combox)
        # 状态
        item_status = QTableWidgetItem(str(status))
        self.tw_citan_data.setItem(row_count, 7, item_status)
        item_status.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tw_citan_ref()

    def tw_citan_ref(self):
        self.tw_citan_data.resizeColumnsToContents()
        self.tw_citan_data.resizeRowsToContents()

    def on_bt_task_up_clicked(self):
        row_count = self.tw_citan_data.rowCount()
        data = []
        for row in range(row_count):
            if row < 0:
                continue
            row_data = {
                "task_id": self.tw_citan_data.item(row, 0).text(),
                "acc": self.tw_citan_data.item(row, 1).text(),
                "acc_pas": self.tw_citan_data.item(row, 2).text(),
                "acc_server1": self.tw_citan_data.item(row, 3).text(),
                "acc_server2": self.tw_citan_data.item(row, 4).text(),
                "start_time": self.tw_citan_data.cellWidget(row, 6).currentText(),
            }
            data.append(row_data)
        syn = {
                "call_back":socket_msg.update_citan_task,
                "data":data
            }
        WebSocketClient.send_json(syn)
    
    def on_del_task_clicked(self):
        del_index = self.tw_citan_data.currentRow()
        if del_index >=0:
            self.tw_citan_data.removeRow(del_index)
    
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
            gbd.main_window_hwnd = int(self.cbb_main_win.currentText())
        else:
            gbd.main_window_hwnd = 0
    
    def on_cbb_main_win_index_changed(self):
        hwnd = self.cbb_main_win.currentText()
        Controls.flash_hwnd(int(hwnd))
    
    # 刷新按键循环下拉框
    def refresh_key_range_combox(self):
        key_list = list(win_key_dc.keys())
        self.cbb_key.addItems(key_list)

    def thread_key_range_done(self):
        self.bt_start_range_key.setText("开始循环")
        self.bt_start_range_key.setEnabled(True)