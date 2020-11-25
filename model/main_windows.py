import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from model.form_login import LoginForm
from model.form_main import MainForm
import json
from lib.ui_lib import BaseForm
from lib import global_data as gbd
from model import md_user

class MainWiondows(QMainWindow,BaseForm):

    def closeEvent(self, event):
        super(BaseForm,self).closeEvent(event)

    def init_form(self):
        self.login_widget = LoginForm()
        self.login_widget.init()

        self.main_widget = MainForm()
        self.main_widget.init()

        self.init_call_back()

    def init_call_back(self):
        self.login_widget.bt_login.clicked.connect(self.on_bt_login_clicked)
        self.login_widget.bt_register.clicked.connect(self.on_bt_register_clicked)

    def on_bt_login_clicked(self):
        user_name = self.le_user_name.text()
        user_pas = self.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.lb_log.setText("登录失败，用户名或密码不能为空")
            return
        try:
            data = md_user.do_login(user_name, user_pas)
            if data.get("status_code") == 200:
                data = json.loads(data)
                gbd.user_data = gbd.UserData(**data)
                print("跳转到页面")
            else:
                data = json.loads(data["datas"])
                self.lb_log.setText(data.get("msg",""))
                self.widget.hide()
                self.main_widget.widget.show()
        except Exception as identifier:
            self.lb_log.setText(str(identifier))
        # gbd.Exit = True
        # start_thread()

    def on_bt_register_clicked(self):
        user_name = self.le_user_name.text()
        user_pas = self.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.lb_log.setText("注册失败，用户名或密码不能为空")
            return
        ret = md_user.do_register(user_name, user_pas)
        data = ret.get("datas",None)
        if data is None:
            self.lb_log.setText("网络错误")
        else:
            data = json.loads(data)
            self.lb_log.setText(data.get("msg",""))



def show_login():
    app = QApplication(sys.argv)
    MainWindow = MainWiondows()
    MainWindow.init_form()
    MainWindow.login_widget.show_ui()
    sys.exit(app.exec_())
