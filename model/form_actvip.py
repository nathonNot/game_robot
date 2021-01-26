from qt_ui.Ui_actvip import Ui_ActVipForm
from lib.ui_lib import BaseForm
import requests
import config
from lib import global_data as gbd
import json
from model import md_user

# 激活vip
class ActVipForm(Ui_ActVipForm,BaseForm):

    isDialog = True

    def setupUi(self, Form):
        super().setupUi(Form)

    def init(self):
        super().init()
        self.bt_act.clicked.connect(self.on_bt_act_clicked)

    def on_bt_act_clicked(self):
        act_code = self.le_act_code.text()
        if len(act_code) != 36:
            self.lb_log.setText("激活码格式不正确")
            return
        url = config.base_url + "/api/couponse/activate"
        data = {
            "user_id":gbd.user_data.user_id,
            "couponse_id":act_code
        }
        res = requests.post(url,json=data)
        if res.status_code != 200:
            self.lb_log.setText(res.text)
            return
        res_data = res.json()
        self.lb_log.setText(res_data['msg'])
        data = md_user.do_login(gbd.user_data.user_name, gbd.user_data.user_pass)
        msg_data = json.loads(data["datas"])
        if data.get("status_code") == 200:
            gbd.user_data = gbd.UserData(**msg_data)
            gbd.MainWindow.main_widget.show_ui()