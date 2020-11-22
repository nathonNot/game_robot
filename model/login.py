from qt_ui.Ui_login import Ui_LoginForm
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from lib.utils import start_thread
import os
import lib.global_data as gbd

class LoginForm(Ui_LoginForm):

    def setupUi(self,LoginForm):
        super().setupUi(LoginForm)
        self.bt_login.clicked.connect(self.on_bt_login_clicked)
        self.bt_register.clicked.connect(self.on_bt_register_clicked)
    
    def on_bt_login_clicked(self):
        user_name = self.le_user_name.text()
        user_pas = self.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.lb_log.setText("登录失败，用户名或密码不能为空")
        print("登录")
        start_thread()

    
    def on_bt_register_clicked(self):
        user_name = self.le_user_name.text()
        user_pas = self.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.lb_log.setText("注册失败，用户名或密码不能为空")
        print("注册")


class MainWiondows(QMainWindow):

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QMessageBox.question(self,
        '本程序',
        "是否要退出程序？",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            gbd.Exit = False
            for t in gbd.threads:
                t.join()
            os._exit(0)
        else:
            event.ignore()


def show_login():
    app = QApplication(sys.argv)
    MainWindow = MainWiondows()
    ui = LoginForm()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_()) 


if __name__ == "__main__":
    login = Ui_LoginForm()
    login.show()
    