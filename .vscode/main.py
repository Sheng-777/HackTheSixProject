import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QPixmap
from PyQt5.QtCore import QBasicTimer
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
        
        self.enterSumm.returnPressed.connect(self.searchSumm)
        self.go.clicked.connect(self.searchSumm)
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(100, 650, 900, 10)
        self.pbar.hide()

        self.timer = QBasicTimer()
        self.step = 0
        
        self.show()

    def timerEvent(self, e):

        if self.step >= 100:
            self.timer.stop()
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def searchSumm(self):
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
            self.pbar.show()
            self.timer.start(100, self)
        
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()
   
if __name__ == '__main__':
    main()
