import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QBasicTimer
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
        
        self.label = QLabel(self)
        # loading image
        p = os.path.abspath("adcdifflogo.png")
        self.pixmap = QPixmap(str(p))
        self.pixmap = self.pixmap.scaled(400,260)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.label.move(300,0)       
        
        self.players = []
        self.enterSumm.setFocus()
        
        self.pastResult = QLabel(self)
        self.pastResult.setFont(QFont("Bodoni MT",14))
        self.pastResult.setText("Past Result:")
        self.pastResult.move(10,325)
        self.pastResult.adjustSize()
        
        self.show()
        self.getPast()
        
        self.enterSumm.returnPressed.connect(self.searchSumm)
        self.go.clicked.connect(self.searchSumm)
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(100, 750, 800, 10)
        self.pbar.hide()

        self.timer = QBasicTimer()
        self.step = 0
        
        self.show()


    def timerEvent(self, e):

        if self.step >= 100:
            self.timer.stop()
            self.step = 0
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
            #print('Summoner name: ' + summText) <-- to check if program works
            #print('Region: ' + region)
            self.pbar.show()
            self.timer.start(100, self)
        
            playerSummary = InfoGet(summText,region,10)
            
            if playerSummary == "User Not Found":
                self.enterSumm.clear()
                pass
            
            elif playerSummary not in self.players[-3:]:
                playerInfo = QLabel(self)
                #print("hi")
                playerInfo.setWordWrap(True)
                playerInfo.move(40,360+(130*(len(self.players)%3)))
                playerInfo.setFixedWidth(900)
                playerInfo.setFont(QFont("Bodoni MT",10))
                playerInfo.setText(f"Summoner Name: {playerSummary['playerName']} | Win%: {playerSummary['winPercentage'] * 100}% | W/L : {playerSummary['recentWin']} / {playerSummary['recentLose']} \nComment: {playerSummary['comment']}")
                playerInfo.adjustSize()
                playerInfo.setStyleSheet("border : 1px solid black;")
                self.players.append(playerSummary)
                
                f = open(Path("pastHistory.txt"),"a")
                f.write(f"{summText}|{region} \n")
                
                if(len(self.players) > 6):
                    self.players.pop(0)
                    self.players.pop(0)
                    self.players.pop(0)
                
                playerInfo.show()
                self.enterSumm.clear()


    def getPast(self):
        f = open(Path("pastHistory.txt"),"r")
        for x in f.readlines()[-3:]:
            sName, sRegion = x.split("|")[0].strip(), x.split("|")[1].strip()
            playerSum = InfoGet(sName,sRegion,10)
            self.displayInfo(playerSum)
            
        
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()
   
if __name__ == '__main__':
    main()
