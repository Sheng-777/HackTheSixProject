import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    WinW = 800
    WinH = 800
    win.setGeometry(int(width/2 - WinW/2), int(height/2 - WinH/2), WinW, WinH)
    win.setWindowTitle("ADCDIFF.gg")
    win.show()
    sys.exit(app.exec_())
    
window()