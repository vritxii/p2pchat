from PyQt5.QtWidgets import *  
from PyQt5.QtCore import *  

class SinClass(QObject):
      
    ##声明一个无参数的信号
    sin1 = pyqtSignal()
      
    ##声明带一个int类型参数的信号
    sin2 = pyqtSignal(int)
      
    ##声明带一个int和str类型参数的信号
    sin3 = pyqtSignal(int,str)
  
    ##声明带一个列表类型参数的信号
    sin4 = pyqtSignal(list)
  
    ##声明带一个字典类型参数的信号
    sin5 = pyqtSignal(dict)
  
    ##声明一个多重载版本的信号，包括了一个带int和str类型参数的信号，以及带str参数的信号
    sin6 = pyqtSignal([int,str], [str])
      
    def __init__(self,parent=None):
        super(SinClass,self).__init__(parent)
  
        ##信号连接到指定槽
        self.sin1.connect(self.sin1Call)
        self.sin2.connect(self.sin2Call)
        self.sin3.connect(self.sin3Call)
        self.sin4.connect(self.sin4Call)
        self.sin5.connect(self.sin5Call)
        self.sin6[int,str].connect(self.sin6Call)
        self.sin6[str].connect(self.sin6OverLoad)
  
        ##信号发射
        self.sin1.emit()
        self.sin2.emit(1)
        self.sin3.emit(1,"text")
        self.sin4.emit([1,2,3,4])
        self.sin5.emit({"name":"codeio","age":"25"})
        self.sin6[int,str].emit(1,"text")
        self.sin6[str].emit("text")
          
    def sin1Call(self):
        print("sin1 emit")
  
    def sin2Call(self,val):
        print("sin2 emit,value:",val)
  
    def sin3Call(self,val,text):
        print("sin3 emit,value:",val,text)
  
    def sin4Call(self,val):
        print("sin4 emit,value:",val)
          
    def sin5Call(self,val):
        print("sin5 emit,value:",val)
  
    def sin6Call(self,val,text):
        print("sin6 emit,value:",val,text)
  
    def sin6OverLoad(self,val):
        print("sin6 overload emit,value:",val)
  
sin = SinClass()