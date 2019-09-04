import os, sys
import matplotlib.pyplot as plt
from multiprocessing import Process
from threading import Thread
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
# import win32api, win32con

from AboutGui import About
from CalcOndurationGui import OndurationGui
from DrxDefine import *
from DrxProc import DrxFileParser, DrxLeftDataProc, ClearListData
from UDP import UDP

qtCreatorFile = "DrxGUI.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setWindowIcon(QIcon("drxGui.ico"))

        self.setupUi(self)

        self.infomation = "DRX探索版，\n正式版本敬请期待！"

        self.cwd = os.getcwd() + "/log"
        self.aboutGui = About()
        self.ondurationGui = OndurationGui()
        self.udp = UDP()

        self.pushButton_chooseFile.clicked.connect(self.chooseFile)
        self.pushButton_chooseDir.clicked.connect(self.chooseDir)
        self.pushButton_draw.clicked.connect(self.drawDrxPlot)
        self.pushButton_draw_clear.clicked.connect(self.clearAllFigure)

        self.spinBox_TtiTime.valueChanged.connect(lambda : self.spinTimeCalc("tti"))
        self.spinBox_Frame.valueChanged.connect(lambda : self.spinTimeCalc("frame"))
        self.spinBox_Slot.valueChanged.connect(lambda : self.spinTimeCalc("slot"))
        self.spinBox_RadioTime.valueChanged.connect(lambda : self.spinTimeCalc("radio"))

        self.menu_help.triggered[QtWidgets.QAction].connect(self.helpMenu)
        self.menu_file.triggered[QtWidgets.QAction].connect(self.fileMenu)
        self.pushButton_test.clicked.connect(lambda: self.test("11"))
        self.pushButton_test_2.clicked.connect(lambda: self.test("22"))

        self.statusbar.showMessage("DRX LOG 解析")
        self.udp.sendToServer(("[Start] Version:%s") %(VERSION))

        self.startUdpSer()

    def startUdpSer(self):
        self.t = Thread(target=self.receiveFromServerMsg, args=())
        self.t.start()

    def receiveFromServerMsg(self):
        while True:
            data = self.udp.receiveFromServer()
            if data is None:
                break
            if data == QUERY_DRX_CLIENT_STATE:
                self.udp.sendToServer(("response [Start] Version:%s") % (VERSION))
            else:
                self.statusbar.showMessage(data)
                self.infomation = data

    def spinTimeCalc(self, type):
        print("type = ", type)
        if type == "tti":
            ttiTime = self.spinBox_TtiTime.value()
            print("TTI time = %d" % ttiTime)
            frame = ttiTime // SLOT_PER_FRAME
            slot = ttiTime % SLOT_PER_FRAME
            radioTime = (frame << 8) + slot
            self.spinBox_Frame.setValue(frame)
            self.spinBox_Slot.setValue(slot)
            self.spinBox_RadioTime.setValue(radioTime)

        if type == "frame" or type == "slot":
            frame = self.spinBox_Frame.value()
            slot = self.spinBox_Slot.value()
            print("Frame = %d, Slot = %d" % (frame, slot))
            ttiTime = frame * SLOT_PER_FRAME + slot
            radioTime = (frame << 8) + slot
            self.spinBox_TtiTime.setValue(ttiTime)
            self.spinBox_RadioTime.setValue(radioTime)

        if type == "radio":
            radioTime = self.spinBox_RadioTime.value()
            print("Radio time = %d" % (radioTime))
            frame = radioTime >> 8
            slot = radioTime & 0xFF
            ttiTime = frame * SLOT_PER_FRAME + slot

            self.spinBox_TtiTime.setValue(ttiTime)
            self.spinBox_Frame.setValue(frame)
            self.spinBox_Slot.setValue(slot)

    def test(self, n):
        a = self.checkBox_onduration.isChecked()
        b = self.spinBox_TtiTime.value()
        fileName = self.lineEdit_fileName.text().strip()
        dirName = self.lineEdit_DirName.text().strip()
        print(a, b)
        c = os.path.isfile(fileName)
        d = os.path.isdir(dirName)
        print(c, d)
        self.textBrowser_output.append("Button {0} test".format(n))

    def helpMenu(self, q):
        self.statusbar.showMessage(q.text())
        if q.text() == "关于":
            self.aboutGui.show()

    def fileMenu(self, q):
        self.statusbar.showMessage(q.text())
        if q.text() == "Onduration计算工具":
            self.ondurationGui.show()
        if q.text() == "打开文件":
            QMessageBox.warning(self, "提示", self.infomation, QMessageBox.Ok)
            # win32api.MessageBox(0, self.infomation, "提示", win32con.MB_ICONINFORMATION)

    def chooseFile(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", self.cwd, "All Files (*);;Text Files (*.txt)")
        if fileName != "":
            self.lineEdit_fileName.setText(fileName)
            self.radioButton_choseFile.setChecked(True)
            self.cwd = os.path.dirname(fileName)

    def chooseDir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", self.cwd)
        if dir != "":
            self.lineEdit_DirName.setText(dir)
            self.radioButton_choseDir.setChecked(True)
            self.cwd = dir

    def drawFile(self, fileName):
        print("draw in")
        DrxFileParser(fileName, self.checkBox_onduration.isChecked(), self.checkBox_Inactivity.isChecked(),
                      self.checkBox_UlReTx.isChecked(), self.checkBox_DlReTx.isChecked(), self.textBrowser_output)
        DrxLeftDataProc(self.textBrowser_output)
        plt.show()
        print("draw out")

    def drawDirFileList(self, dirName):
        print("draw in")
        fileList = os.listdir(dirName)
        for list in fileList:
            path = os.path.join(dirName, list)
            if os.path.isfile(path) and os.path.splitext(path)[1] == ".txt":
                print(path)
                self.textBrowser_output.append(path)
                DrxFileParser(path, self.checkBox_onduration.isChecked(), self.checkBox_Inactivity.isChecked(),
                              self.checkBox_UlReTx.isChecked(), self.checkBox_DlReTx.isChecked(),
                              self.textBrowser_output)
        DrxLeftDataProc(self.textBrowser_output)
        plt.show()
        print("draw out")

    def drawDrxPlot(self):
        ClearListData()
        plt.close('all')
        fileName = self.lineEdit_fileName.text().strip()
        dirName = self.lineEdit_DirName.text().strip()
        if self.radioButton_choseFile.isChecked():
            if not os.path.isfile(fileName):
                QMessageBox.warning(self,"警告","文件不存在!",QMessageBox.Ok)
                # win32api.MessageBox(0, "文件不存在!", "警告", win32con.MB_ICONWARNING)
            else:
                print(fileName)
                self.textBrowser_output.append(fileName)
                self.p = Process(target=self.drawFile, args=(fileName,))
                self.p.run()
        elif self.radioButton_choseDir.isChecked():
            if not os.path.exists(dirName):
                QMessageBox.warning(self,"警告","文件夹不存在!",QMessageBox.Ok)
                # win32api.MessageBox(0, "文件夹不存在!", "警告", win32con.MB_ICONWARNING)
            else:
                print(dirName)
                self.textBrowser_output.append(dirName)
                self.p = Process(target=self.drawDirFileList, args=(dirName,))
                self.p.run()

    def clearAllFigure(self):
        print("close start")
        plt.close('all')
        self.textBrowser_output.setText("")
        print("close end")

    # 界面退出时执行
    def closeEvent(self, *args, **kwargs):
        self.clearAllFigure()
        self.aboutGui.close()
        self.ondurationGui.close()
        self.udp.sendToServer(("[End] Version:%s") %(VERSION))
        self.udp.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
