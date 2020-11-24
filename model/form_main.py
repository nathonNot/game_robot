from qt_ui.Ui_main import Ui_main
from PyQt5.QtWidgets import QWidget
from lib.ui_lib import BaseForm

class MainForm(Ui_main,BaseForm):

    def setupUi(self, LoginForm):
        super().setupUi(LoginForm)

    def update(self):
        pass