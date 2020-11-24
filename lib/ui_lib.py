from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QWidget
import lib.global_data as gbd
import os

class BaseForm():
    
    def show_ui(self):
        self.widget.show()

    def init(self):
        self.widget = QWidget()
        self.setupUi(self.widget)
        self.widget.closeEvent = self.closeEvent

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        # reply = QMessageBox.question(
        #     self, "本程序", "是否要退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        # )
        # if reply == QMessageBox.Yes:
        event.accept()
        gbd.Exit = False
        for t in gbd.threads:
            t.join()
        os._exit(0)
        # else:
        #     event.ignore()