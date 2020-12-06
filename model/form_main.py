from qt_ui.Ui_main import Ui_main
from lib.ui_lib import BaseForm
from lib import global_data as gbd
import webbrowser
from lib.thread_class import WebSocketThread,MainRefresh
from lib.utils import start_thread,thread_stop

class MainForm(Ui_main,BaseForm):

    def setupUi(self, LoginForm):
        super().setupUi(LoginForm)

    def show_ui(self):
        self.lb_user_name.setText(gbd.user_data.user_name)
        self.bt_chongzhi.setVisible(False)
        self.widget.show()

    def init_callback(self):
        self.bt_chongzhi.clicked.connect(self.open_chongzhi)
        self.bt_ws_con.clicked.connect(self.on_bt_ws_con_clicked)

        self.cb_tuanlian.clicked.connect(
            self.on_cb_tuanlian_clicked)
        self.cb_neigong.clicked.connect(self.on_cb_neigong_clicked)
        self.bt_start_up.clicked.connect(
            self.on_bt_start_up_clicked)

    def open_chongzhi(self):
        url = "www.baidu.com"
        webbrowser.open(url)
    
    def on_cb_neigong_clicked(self):
        gbd.module_dc["内功"].is_act = self.cb_neigong.isChecked()

    def on_cb_tuanlian_clicked(self):
        gbd.module_dc["团练"].is_act = self.cb_tuanlian.isChecked()

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
