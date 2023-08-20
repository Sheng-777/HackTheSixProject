import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QPixmap
from pathlib import Path
from getInfo import InfoGet

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
        
        self.players = []
        
        self.show()
        self.enterSumm.returnPressed.connect(self.searchSumm)
        self.go.clicked.connect(self.searchSumm)

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
            
            playerSummary = InfoGet(summText,region,10)
            if playerSummary not in self.players:
                playerInfo = QLabel(self)
                print("hi")
                playerInfo.setWordWrap(True)
                playerInfo.move(40,340+(125*(len(self.players)%3)))
                playerInfo.setFixedWidth(900)
                playerInfo.setFont(QFont("Bodoni MT",10))
                playerInfo.setText(f"Summoner Name: {playerSummary['playerName']} | Win%: {playerSummary['winPercentage'] * 100}% | W/L : {playerSummary['recentWin']} / {playerSummary['recentLose']} \nComment: {playerSummary['comment']}")
                playerInfo.adjustSize()
                self.players.append(playerSummary)
                playerInfo.show()
                self.enterSumm.clear()
                  

            
        
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()
   
if __name__ == '__main__':
    main()
