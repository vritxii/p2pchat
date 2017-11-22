import client_ui
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = client_ui.Main_Window()
    sys.exit(app.exec_())