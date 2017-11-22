import sys  
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget  
class Example(QWidget):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  
  
  
    def initUI(self):  
        self.resize(250, 150)  
        self.center()  
        self.setWindowTitle('窗口定在屏幕中心')  
        self.show()  
    def center(self):  
        qr = self.frameGeometry()  
        cp = QDesktopWidget().availableGeometry().center()  
        qr.moveCenter(cp)  
        self.move(qr.topLeft())  
  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    ex = Example()  
    sys.exit((app.exec_()))
