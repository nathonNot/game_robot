import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QWidget
from model.form_login import LoginForm
from model.form_main import MainForm
from lib.ui_lib import BaseForm

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
        self.login_widget.enter_succes_func = self.to_main

    def to_main(self):
        self.main_widget.widget.show()


def show_login():
    app = QApplication(sys.argv)
    MainWindow = MainWiondows()
    MainWindow.init_form()
    MainWindow.login_widget.show_ui()
    sys.exit(app.exec_())
