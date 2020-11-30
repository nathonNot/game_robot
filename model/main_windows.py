import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from model.form_login import LoginForm
from model.form_main import MainForm
import json
from lib.ui_lib import BaseForm
from lib import global_data as gbd
from model import md_user
from lib.utils import start_thread


class MainWiondows(QMainWindow, BaseForm):

    log_q = []

    def closeEvent(self, event):
        super(BaseForm, self).closeEvent(event)

    def init_form(self):
        self.login_widget = LoginForm()
        self.login_widget.init()

        self.main_widget = MainForm()
        self.main_widget.init()

        self.init_call_back()

    def init_call_back(self):
        gbd.main_log_info_call_back = self.log_print
        self.login_widget.bt_login.clicked.connect(self.on_bt_login_clicked)
        self.login_widget.bt_register.clicked.connect(
            self.on_bt_register_clicked)
        self.main_widget.cb_tuanlian.clicked.connect(
            self.on_cb_tuanlian_clicked)
        self.main_widget.cb_neigong.clicked.connect(self.on_cb_neigong_clicked)
        self.main_widget.bt_start_up.clicked.connect(
            self.on_bt_start_up_clicked)

    def on_bt_login_clicked(self):
        user_name = self.login_widget.le_user_name.text()
        user_pas = self.login_widget.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.login_widget.lb_log.setText("登录失败，用户名或密码不能为空")
            return
        try:
            data = md_user.do_login(user_name, user_pas)
            msg_data = json.loads(data["datas"])
            if data.get("status_code") == 200:
                gbd.user_data = gbd.UserData(**msg_data)
                self.login_widget.widget.hide()
                self.main_widget.show_ui()
            else:
                self.login_widget.lb_log.setText(msg_data.get("msg", ""))
        except Exception as identifier:
            self.login_widget.lb_log.setText(str(identifier))

    def on_bt_register_clicked(self):
        user_name = self.login_widget.le_user_name.text()
        user_pas = self.login_widget.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.login_widget.lb_log.setText("注册失败，用户名或密码不能为空")
            return
        ret = md_user.do_register(user_name, user_pas)
        data = ret.get("datas", None)
        if data is None:
            self.login_widget.lb_log.setText("网络错误")
        else:
            data = json.loads(data)
            self.login_widget.lb_log.setText(data.get("msg", ""))

    def on_cb_neigong_clicked(self):
        gbd.module_dc["内功"].is_act = self.main_widget.cb_neigong.isChecked()

    def on_cb_tuanlian_clicked(self):
        gbd.module_dc["团练"].is_act = self.main_widget.cb_tuanlian.isChecked()

    def on_bt_start_up_clicked(self):
        if gbd.Exit:
            gbd.Exit = False
            for t in gbd.threads:
                t.join()
            self.main_widget.bt_start_up.setText("启动")
        else:
            self.main_widget.bt_start_up.setText("停止")
            for t in gbd.threads:
                t.join()
            gbd.Exit = True
            start_thread()

    def log_print(self, log_info):
        if len(self.log_q) > 1:
            self.log_q.pop(0)
        self.log_q.append(log_info)
        self.main_widget.lb_log.setText("\n".join(self.log_q))


def show_login():
    app = QApplication(sys.argv)
    MainWindow = MainWiondows()
    MainWindow.init_form()
    MainWindow.login_widget.show_ui()
    sys.exit(app.exec_())
