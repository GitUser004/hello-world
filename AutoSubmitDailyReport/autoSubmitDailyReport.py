import sys,threading,time
from PyQt5 import QtCore, uic, QtWidgets
import pyautogui


qtCreatorFile = "autoSubmitDailyReport.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        QtWidgets.QMainWindow.setWindowFlags(self,QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        self.X_lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Y_lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)

        self.desktop = QtWidgets.QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.desktopHeigh = self.screenRect.height()
        self.desktopWidth = self.screenRect.width()
        print(self.desktopWidth)
        print(self.desktopHeigh)

        self.timer = None
        self.delayCnt = 0

        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = False

        self.pushButton_start.clicked.connect(self.start)

    def keepDesktopAlive(self):
        pyautogui.click(0, self.desktopHeigh - 1)
        time.sleep(0.1)
        pyautogui.click(0, self.desktopHeigh - 1)

    def startDelayTimer(self):
        self.delayCnt += 1
        if self.delayCnt <= self.delay:
            self.timer = threading.Timer(60, self.startDelayTimer)
            self.timer.start()
            print(time.strftime('%Y-%m-%d %H:%M:%S') + " id %d" %(self.timer.ident))
            self.label_state.setText("剩余 %d 分钟..." %(self.delay - self.delayCnt + 1))
            if self.delayCnt % 2 == 0 and self.checkBox_keepDesktopAlive.isChecked():
                self.keepDesktopAlive()
        else:
            self.timerOut()

    def timerOut(self):
        print("timeout id %d" %(self.timer.ident))
        self.label_state.setText("开始提交日报！")
        print('web x, y = %d, %d' % (self.web_x, self.web_y))
        # pyautogui.moveTo(self.web_x, self.web_y, duration=2)
        time.sleep(1)
        pyautogui.click(self.web_x, self.web_y)

        print('submit x, y = %d, %d' % (self.submit_x, self.submit_y))
        # pyautogui.moveTo(self.submit_x, self.submit_y, duration=2)
        time.sleep(1)
        pyautogui.click(self.submit_x, self.submit_y)

        print('ok x, y = %d, %d' % (self.ok_x, self.ok_y))
        # pyautogui.moveTo(self.ok_x, self.ok_y, duration=2)
        time.sleep(1)
        pyautogui.click(self.ok_x, self.ok_y)

        self.pushButton_start.setText("开始")
        self.label_state.setText("完成")


    def start(self):
        if self.pushButton_start.text() == "开始":
            self.pushButton_start.setText("取消")
            self.web_x = int(self.lineEdit_web_x.text())
            self.web_y = int(self.lineEdit_web_y.text())

            self.submit_x = int(self.lineEdit_submit_x.text())
            self.submit_y = int(self.lineEdit_submit_y.text())

            self.ok_x = int(self.lineEdit_ok_x.text())
            self.ok_y = int(self.lineEdit_ok_y.text())

            self.delay = int(self.lineEdit_delay.text())
            self.delayCnt = 0

            self.startDelayTimer()

        elif self.pushButton_start.text() == "取消":
            self.pushButton_start.setText("开始")
            self.label_state.setText("取消!")
            threadId = self.timer.ident
            self.timer.cancel()
            print("timer id %d is cancled !" %(threadId))

    def mouseMoveEvent(self, e):
        x = e.globalPos().x()
        y = e.globalPos().y()
        self.X_lcdNumber.display(x)
        self.Y_lcdNumber.display(y)

    def mousePressEvent(self, e):
        print('mousePressEvent(%d,%d)\n' % (e.globalPos().x(), e.globalPos().y()))

    def mouseReleaseEvent(self, e):
        print('mouseReleaseEvent(%d,%d)\n' % (e.globalPos().x(), e.globalPos().y()))

    # 界面退出时执行
    def closeEvent(self, *args, **kwargs):
        if self.timer and self.timer.isAlive():
            threadId = self.timer.ident
            self.timer.cancel()
            print("timer id %d is cancled !" % (threadId))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

