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
        #uic.loadUi(r"C:\Users\alexj\OneDrive\Documents\GitHub\HackTheSixProject\adcdiffgg.ui", self)
        #uic.loadUi("adcdiffgg.ui", self)
        #screen_resolution = application.desktop().screenGeometry()
        #width, height = screen_resolution.width(), screen_resolution.height()
        
        #self.setGeometry(int(width/2 - WinW/2), int(height/2 - WinH/2))
        self.setWindowTitle("ADCDIFF.gg")
        self.setToolTip("ADCdiff.gg")
        
        # create logo image
        self.label = QLabel(self)
        # loading image
        p = os.path.abspath("adcdifflogo.png")
        self.pixmap = QPixmap(str(p))
        #self.pixmap = QPixmap(r'C:\Users\alexj\OneDrive\Documents\GitHub\HackTheSixProject\adcdifflogo.png')
        #self.pixmap = QPixmap('adcdifflogo.png')
        self.pixmap = self.pixmap.scaled(400,200)
        # adding image to label
        self.label.setPixmap(self.pixmap)
        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.label.move(300,20)       

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
            print('Summoner name: ' + summText)
            print('Region: ' + region)
        
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()
   
if __name__ == '__main__':
    main()
