import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QPixmap
from pathlib import Path

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        p = Path("adcdiffgg.ui").resolve()
        uic.loadUi(str(p),self)
        
        self.setWindowTitle("ADCDIFF.gg")
        self.setToolTip("ADCdiff.gg")
        
        p = Path("adcdifficon.png").resolve()
        self.setWindowIcon(QIcon(str(p)))
        
        # create logo image
        self.label = QLabel(self)
        # loading image
        p = os.path.abspath("adcdifflogo.png")
        self.pixmap = QPixmap(str(p))
        self.pixmap = self.pixmap.scaled(400,260)
        # adding image to label
        self.label.setPixmap(self.pixmap)
        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.label.move(300,0)       
        self.show()
        self.enterSumm.returnPressed.connect(self.enter)
        self.go.clicked.connect(self.clicked)

    def clicked(self):
        summText = self.enterSumm.text()
        region = self.enterReg.currentText()
        if summText == "":
            message = QMessageBox()
            message.setWindowTitle("Invalid operation")
            message.setText("Please enter a Summoner name")
            message.exec_()
        else:
            print('Summoner name: ' + summText)
            print('Region: ' + region)
        
    def enter(self):
        summText = self.enterSumm.text()
        region = self.enterReg.currentText()
        print('Summoner name: ' + summText)
        print('Region: ' + region)
        
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()
   
if __name__ == '__main__':
    main()
