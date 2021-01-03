from qt_ui.Ui_caiji import Ui_CaiJiForm
from lib.ui_lib import BaseForm

class CaiJiForm(Ui_CaiJiForm,BaseForm):

    isDialog = True

    def setupUi(self, Form):
        super().setupUi(Form)