# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\project\python\jiuyin_robot\qt_ui\login.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(582, 420)
        self.bt_login = QtWidgets.QPushButton(LoginForm)
        self.bt_login.setGeometry(QtCore.QRect(200, 250, 75, 23))
        self.bt_login.setObjectName("bt_login")
        self.bt_register = QtWidgets.QPushButton(LoginForm)
        self.bt_register.setGeometry(QtCore.QRect(310, 250, 75, 23))
        self.bt_register.setObjectName("bt_register")
        self.lb_log = QtWidgets.QLabel(LoginForm)
        self.lb_log.setGeometry(QtCore.QRect(190, 40, 211, 61))
        self.lb_log.setText("")
        self.lb_log.setObjectName("lb_log")
        self.le_user_name = QtWidgets.QLineEdit(LoginForm)
        self.le_user_name.setGeometry(QtCore.QRect(260, 140, 131, 31))
        self.le_user_name.setObjectName("le_user_name")
        self.le_user_pas = QtWidgets.QLineEdit(LoginForm)
        self.le_user_pas.setGeometry(QtCore.QRect(260, 190, 131, 31))
        self.le_user_pas.setObjectName("le_user_pas")
        self.label = QtWidgets.QLabel(LoginForm)
        self.label.setGeometry(QtCore.QRect(190, 140, 51, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(LoginForm)
        self.label_2.setGeometry(QtCore.QRect(190, 200, 41, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(LoginForm)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "登录"))
        self.bt_login.setText(_translate("LoginForm", "登录"))
        self.bt_register.setText(_translate("LoginForm", "注册"))
        self.label.setText(_translate("LoginForm", "用户名"))
        self.label_2.setText(_translate("LoginForm", "密码"))
