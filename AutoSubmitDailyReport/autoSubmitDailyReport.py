
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import pyautogui


qtCreatorFile = "autoSubmitDailyReport.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.X_lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Y_lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)

        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = False

        self.pushButton_start.clicked.connect(self.setMousePos)

    def setMousePos(self):
        x = int(self.X_lineEdit.text())
        y = int(self.Y_lineEdit.text())
        print('x, y = %d, %d\n' %(x,y))
        pyautogui.moveTo(x, y, duration=10)

    def mouseMoveEvent(self, e):
        x = e.globalPos().x()
        y = e.globalPos().y()
        self.X_lcdNumber.display(x)
        self.Y_lcdNumber.display(y)

    def mousePressEvent(self, e):
        print('mousePressEvent(%d,%d)\n' % (e.globalPos().x(), e.globalPos().y()))

    def mouseReleaseEvent(self, e):
        print('mouseReleaseEvent(%d,%d)\n' % (e.globalPos().x(), e.globalPos().y()))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

