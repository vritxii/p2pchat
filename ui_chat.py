# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Chat(QtWidgets.QWidget):
    '''
    聊天界面
    '''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Chat")
        MainWindow.resize(949, 661)
        MainWindow.setStyleSheet("background-color: rgb(222, 255, 211);\n"
"background-image: url(back1.jpg);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(580, 50, 351, 491))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pub_users = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.pub_users.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pub_users.setObjectName("pub_users")
        self.horizontalLayout.addWidget(self.pub_users)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.add_pri_user = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_pri_user.setObjectName("add_pri_user")
        self.verticalLayout_5.addWidget(self.add_pri_user)
        self.rm_pri_user = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.rm_pri_user.setObjectName("rm_pri_user")
        self.verticalLayout_5.addWidget(self.rm_pri_user)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.pri_users = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.pri_users.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.pri_users.setObjectName("pri_users")
        self.horizontalLayout.addWidget(self.pri_users)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(600, 20, 101, 23))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(820, 20, 101, 23))
        self.label_2.setObjectName("label_2")
        self.label_user = QtWidgets.QLabel(self.centralwidget)
        self.label_user.setGeometry(QtCore.QRect(20, 560, 50, 23))
        self.label_user.setAutoFillBackground(True)
        self.label_user.setStyleSheet("background-color: rgb(255, 170, 255);")
        self.label_user.setObjectName("label_user")
        self.label_tip = QtWidgets.QLabel(self.centralwidget)
        self.label_tip.setGeometry(QtCore.QRect(70, 600, 300, 23))
        self.label_tip.setAutoFillBackground(True)
        self.label_tip.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.label_user.setObjectName("label_user")
        self.msg_show = QtWidgets.QTextBrowser(self.centralwidget)
        self.msg_show.setGeometry(QtCore.QRect(20, 50, 501, 491))
        self.msg_show.setStyleSheet("background-color: rgb(255, 255, 148);")
        self.msg_show.setObjectName("msg_show")
        self.msg_input = QtWidgets.QLineEdit(self.centralwidget)
        self.msg_input.setGeometry(QtCore.QRect(70, 550, 371, 41))
        self.msg_input.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 11pt \"Serif\";\n")
        self.msg_input.setObjectName("msg_input")
        self.send_btu = QtWidgets.QPushButton(self.centralwidget)
        self.send_btu.setGeometry(QtCore.QRect(450, 560, 91, 31))
        self.send_btu.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.send_btu.setObjectName("send_btu")
        self.logout_btu = QtWidgets.QPushButton(self.centralwidget)
        self.logout_btu.setGeometry(QtCore.QRect(840, 560, 91, 31))
        self.logout_btu.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.logout_btu.setObjectName("logout_btu")
        
        self.switch_btu = QtWidgets.QPushButton(self.centralwidget)
        self.switch_btu.setGeometry(QtCore.QRect(720, 560, 91, 31))
        self.switch_btu.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.switch_btu.setObjectName("switch_btu")

        self.welcome_label = QtWidgets.QLabel(self.centralwidget)
        self.welcome_label.setGeometry(QtCore.QRect(90, 10, 246, 32))
        self.welcome_label.setAutoFillBackground(True)
        self.welcome_label.setStyleSheet("background-color: rgb(170, 255, 127);\n"
"font: 16pt \"Noto Sans SC\";")
        self.welcome_label.setObjectName("welcome_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 949, 22))
        self.menubar.setObjectName("menubar")
        self.menuStatus = QtWidgets.QMenu(self.menubar)
        self.menuStatus.setObjectName("menuStatus")
        MainWindow.setMenuBar(self.menubar)
        self.actionlogout = QtWidgets.QAction(MainWindow)
        self.actionlogout.setObjectName("actionlogout")
        self.menuStatus.addAction(self.actionlogout)
        self.menubar.addAction(self.menuStatus.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat"))
        self.add_pri_user.setText(_translate("MainWindow", ">>"))
        self.rm_pri_user.setText(_translate("MainWindow", "<<"))
        self.label.setText(_translate("MainWindow", "Public Users"))
        self.label_2.setText(_translate("MainWindow", "Private Users"))
        self.label_user.setText(_translate("MainWindow", "public:"))
        self.send_btu.setText(_translate("MainWindow", "Send"))
        self.logout_btu.setText(_translate("MainWindow", "logout"))
        self.switch_btu.setText(_translate("MainWindow", "switch"))
        self.welcome_label.setText(_translate("MainWindow", "Hey zt, Welcome to  chat!"))
        self.menuStatus.setTitle(_translate("MainWindow", "Hey, zt"))
        self.actionlogout.setText(_translate("MainWindow", "logout"))
