import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("adcdiffgg.ui", self)
        #screen_resolution = application.desktop().screenGeometry()
        #width, height = screen_resolution.width(), screen_resolution.height()
        
        #self.setGeometry(int(width/2 - WinW/2), int(height/2 - WinH/2))
        #self.setWindowTitle("ADCDIFF.gg")
        #self.setToolTip("ADCdiff.gg")
        self.show()
        self.go.clicked.connect(self.clicked)
        

    def clicked(self):
        summText = self.enterSumm.text()
        region = self.enterReg.currentText()
        if summText == "":
            message = QMessageBox()
            message.setText("Please enter a Summoner name")
            message.exec_()
        else:
            print('button clicked')
            print('Summoner name: ' + summText)
            print('Region: ' + region)
        
    btn_save = QtWidgets.QPushButton(win)
    btn_save.setText('Go')
    btn_save.clicked.connect(clicked)
    btn_save.move(200,130)
    
    win.show()
    sys.exit(app.exec_())
    
window()