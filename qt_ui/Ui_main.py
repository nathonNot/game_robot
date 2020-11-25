# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\project\python\jiuyin_robot\qt_ui\main.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(463, 339)
        self.bt_start_up = QtWidgets.QPushButton(main)
        self.bt_start_up.setGeometry(QtCore.QRect(290, 240, 75, 31))
        self.bt_start_up.setObjectName("bt_start_up")
        self.lb_user_name = QtWidgets.QLabel(main)
        self.lb_user_name.setGeometry(QtCore.QRect(330, 40, 51, 31))
        self.lb_user_name.setObjectName("lb_user_name")
        self.lb_user_vip = QtWidgets.QLabel(main)
        self.lb_user_vip.setGeometry(QtCore.QRect(330, 70, 41, 31))
        self.lb_user_vip.setObjectName("lb_user_vip")
        self.cb_tuanlian = QtWidgets.QCheckBox(main)
        self.cb_tuanlian.setGeometry(QtCore.QRect(40, 100, 101, 31))
        self.cb_tuanlian.setObjectName("cb_tuanlian")
        self.cb_neigong = QtWidgets.QCheckBox(main)
        self.cb_neigong.setGeometry(QtCore.QRect(150, 100, 91, 31))
        self.cb_neigong.setObjectName("cb_neigong")
        self.bt_chongzhi = QtWidgets.QPushButton(main)
        self.bt_chongzhi.setGeometry(QtCore.QRect(370, 80, 75, 23))
        self.bt_chongzhi.setObjectName("bt_chongzhi")
        self.lb_log = QtWidgets.QLabel(main)
        self.lb_log.setGeometry(QtCore.QRect(40, 280, 241, 41))
        self.lb_log.setObjectName("lb_log")

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "设置"))
        self.bt_start_up.setText(_translate("main", "启动"))
        self.lb_user_name.setText(_translate("main", "用户名"))
        self.lb_user_vip.setText(_translate("main", "vip"))
        self.cb_tuanlian.setText(_translate("main", "自动团练授业"))
        self.cb_neigong.setText(_translate("main", "自动点内功"))
        self.bt_chongzhi.setText(_translate("main", "赞助"))
        self.lb_log.setText(_translate("main", "运行日志"))
