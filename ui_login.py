# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

class Ui_Login(QtWidgets.QWidget):
    '''
    登录界面
    '''
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(322, 458)
        Login.setAutoFillBackground(True)
        Login.setStyleSheet("font: 11pt \"Noto Sans SC\";\n"
"background-color: rgb(129, 170, 144);\n"
"")
        self.login_btu = QtWidgets.QPushButton(Login)
        self.login_btu.setGeometry(QtCore.QRect(120, 340, 91, 31))
        self.login_btu.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.login_btu.setObjectName("login_btu")
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(20, 100, 71, 23))
        self.label.setObjectName("label")
        self.server_ip = QtWidgets.QLineEdit(Login)
        self.server_ip.setGeometry(QtCore.QRect(90, 100, 171, 31))
        self.server_ip.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.server_ip.setObjectName("server_ip")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(0, 180, 91, 23))
        self.label_2.setObjectName("label_2")
        self.server_port = QtWidgets.QLineEdit(Login)
        self.server_port.setGeometry(QtCore.QRect(90, 180, 171, 31))
        self.server_port.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.server_port.setObjectName("server_port")
        self.label_3 = QtWidgets.QLabel(Login)
        self.label_3.setGeometry(QtCore.QRect(0, 270, 81, 23))
        self.label_3.setObjectName("label_3")
        self.user_name = QtWidgets.QLineEdit(Login)
        self.user_name.setGeometry(QtCore.QRect(90, 270, 171, 31))
        self.user_name.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.user_name.setObjectName("user_name")
        self.label_4 = QtWidgets.QLabel(Login)
        self.label_4.setGeometry(QtCore.QRect(90, 20, 151, 41))
        self.label_4.setStyleSheet("font: 11pt \"Noto Sans SC\";\n"
"background-color: rgb(255, 170, 127);")
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login"))
        self.login_btu.setText(_translate("Login", "Login"))
        self.label.setText(_translate("Login", "Server IP:"))
        self.label_2.setText(_translate("Login", "Server Port:"))
        self.label_3.setText(_translate("Login", "User Name:"))
        self.label_4.setText(_translate("Login", "              P2P Chat"))
