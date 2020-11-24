from qt_ui.Ui_login import Ui_LoginForm
from lib.utils import start_thread
import lib.global_data as gbd
import requests
import json
from lib.version_authentication import decode_data
from PyQt5.QtWidgets import QWidget
from lib.ui_lib import BaseForm

def do_register(user_name, user_pas):
    data = {"user_name": user_name, "user_pass": user_pas}
    header = {
        "X_Forwarded_For":"192.168.3.89"
    }
    res = requests.post("http://127.0.0.1:8000/api/user/create_user",json=data,headers=header)
    return decode_data(res.text)

def do_login(user_name, user_pas):
    data = {"user_name": user_name, "user_pass": user_pas}
    header = {
        "X_Forwarded_For":"192.168.3.89"
    }
    res = requests.post("http://127.0.0.1:8000/api/user/get_user",json=data,headers=header)
    return decode_data(res.text)

class LoginForm(Ui_LoginForm,BaseForm):

    enter_succes_func = None

    def setupUi(self, LoginForm):
        super().setupUi(LoginForm)
        self.bt_login.clicked.connect(self.on_bt_login_clicked)
        self.bt_register.clicked.connect(self.on_bt_register_clicked)

    def on_bt_login_clicked(self):
        user_name = self.le_user_name.text()
        user_pas = self.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.lb_log.setText("登录失败，用户名或密码不能为空")
            return
        data = do_login(user_name, user_pas)
        if data.get("status_code") == 200:
            data = json.loads(data)
            gbd.user_data = gbd.UserData(**data)
            print("跳转到页面")
        else:
            data = json.loads(data["datas"])
            self.lb_log.setText(data.get("msg",""))
            self.widget.hide()
            self.enter_succes_func()
        gbd.Exit = True
        start_thread()

    def on_bt_register_clicked(self):
        user_name = self.le_user_name.text()
        user_pas = self.le_user_pas.text()
        if user_name == "" or user_pas == "":
            self.lb_log.setText("注册失败，用户名或密码不能为空")
            return
        ret = do_register(user_name, user_pas)
        data = ret.get("datas",None)
        if data is None:
            self.lb_log.setText("网络错误")
        else:
            data = json.loads(data)
            self.lb_log.setText(data.get("msg",""))
    



if __name__ == "__main__":
    login = Ui_LoginForm()
    login.show()
