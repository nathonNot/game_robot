from qt_ui.Ui_main import Ui_main
from PyQt5.QtWidgets import QWidget
from lib.ui_lib import BaseForm
from lib import global_data
import webbrowser

class MainForm(Ui_main,BaseForm):

    def setupUi(self, LoginForm):
        super().setupUi(LoginForm)
        self.init_callback()

    def show_ui(self):
        self.lb_user_name.setText(global_data.user_data.user_name)
        self.bt_chongzhi.setVisible(False)
        self.widget.show()

    def init_callback(self):
        self.bt_chongzhi.clicked.connect(self.open_chongzhi)

    def open_chongzhi(self):
        url = "www.baidu.com"
        webbrowser.open(url)