import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

class my_window(QMainWindow):
    def __int__(self):
        super(my_window, self).__init__()
        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        WinW = 800
        WinH = 800
        self.setGeometry(int(width/2 - WinW/2), int(height/2 - WinH/2), WinW, WinH)
        self.setWindowTitle("ADCDIFF.gg")
        self.setToolTip("ADCdiff.gg")
        #win.setWindowIcon(QIcon('adcdiffgg.jpg')
def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    WinW = 800
    WinH = 800
    win.setGeometry(int(width/2 - WinW/2), int(height/2 - WinH/2), WinW, WinH)
    win.setWindowTitle("ADCDIFF.gg")
    win.setToolTip("ADCdiff.gg")
    #win.setWindowIcon(QIcon('adcdiffgg.jpg')
    
    summ_name = QtWidgets.QLabel(win)
    summ_name.setText('Enter summoner name:')
    summ_name.adjustSize()
    summ_name.move(50,50)
    
    reg_name = QtWidgets.QLabel(win)
    reg_name.setText('Enter region name:')
    reg_name.adjustSize()
    reg_name.move(50,90)
    
    txt_summ = QtWidgets.QLineEdit(win)
    txt_summ.move(200,50)
    
    txt_reg = QtWidgets.QLineEdit(win)
    txt_reg.move(200,90)
    
    def clicked(self):
        print('button clicked')
        print('name: ' + txt_summ.text())
        print('region: ' + txt_reg.text())
        
    btn_save = QtWidgets.QPushButton(win)
    btn_save.setText('Go')
    btn_save.clicked.connect(clicked)
    btn_save.move(200,130)
    
    win.show()
    sys.exit(app.exec_())
    
window()