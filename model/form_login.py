from qt_ui.Ui_login import Ui_LoginForm
from lib.utils import start_thread
import lib.global_data as gbd
import json
from lib.ui_lib import BaseForm

class LoginForm(Ui_LoginForm,BaseForm):


    def setupUi(self, LoginForm):
        super().setupUi(LoginForm)

if __name__ == "__main__":
    login = Ui_LoginForm()
    login.show()
