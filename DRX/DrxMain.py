import os,sys
import matplotlib.pyplot as plt
from multiprocessing import Process
from PyQt5 import QtWidgets, uic
import win32api,win32con

from DrxDefine import *
from DrxProc import DrxFileParser, DrxLeftDataProc, ClearListData



qtCreatorFile = "DrxGUI.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.cwd = os.getcwd()
        self.spinTtiTimeChangeFlag = False
        self.spinFrameSlotChangeFlag = False
        self.spinRadioTimeChangeFlag = False

        self.setupUi(self)
        self.pushButton_chooseFile.clicked.connect(self.chooseFile)
        self.pushButton_chooseDir.clicked.connect(self.chooseDir)
        self.pushButton_draw.clicked.connect(self.drawDrxPlot)
        self.pushButton_draw_clear.clicked.connect(self.clearAllFigure)
        self.spinBox_TtiTime.valueChanged.connect(self.spinTtiTime)
        self.spinBox_Frame.valueChanged.connect(self.spinFrameSlot)
        self.spinBox_Slot.valueChanged.connect(self.spinFrameSlot)
        self.spinBox_RadioTime.valueChanged.connect(self.spnRadioTime)
        self.pushButton_test.clicked.connect(self.test)

    def test(self):
        a=self.checkBox_onduration.isChecked()
        b=self.spinBox_TtiTime.value()
        fileName = self.lineEdit_fileName.text().strip()
        dirName = self.lineEdit_DirName.text().strip()
        print(a,b)
        c=os.path.isfile(fileName)
        d=os.path.isdir(dirName)
        print(c,d)
        self.textBrowser_output.append("124")

    def spinTtiTime(self):
        if not self.spinTtiTimeChangeFlag:
            ttiTime = self.spinBox_TtiTime.value()
            print("TTI time = %d" %(ttiTime))
            frame = ttiTime//SLOT_PER_FRAME
            slot = ttiTime%SLOT_PER_FRAME
            radioTime = (frame<<8) + slot

            self.spinFrameSlotChangeFlag = True
            self.spinRadioTimeChangeFlag = True
            self.spinBox_Frame.setValue(frame)
            self.spinBox_Slot.setValue(slot)
            self.spinBox_RadioTime.setValue(radioTime)
        self.spinTtiTimeChangeFlag = False

    def spinFrameSlot(self):
        if not self.spinFrameSlotChangeFlag:
            frame = self.spinBox_Frame.value()
            slot = self.spinBox_Slot.value()
            print("Frame = %d, Slot = %d" %(frame,slot))
            ttiTime = frame*SLOT_PER_FRAME + slot
            radioTime = (frame<<8) + slot

            self.spinTtiTimeChangeFlag = True
            self.spinRadioTimeChangeFlag = True
            self.spinBox_TtiTime.setValue(ttiTime)
            self.spinBox_RadioTime.setValue(radioTime)
        self.spinFrameSlotChangeFlag = False

    def spnRadioTime(self):
        if not self.spinRadioTimeChangeFlag:
            radioTime = self.spinBox_RadioTime.value()
            print("Radio time = %d" %(radioTime))
            frame = radioTime>>8
            slot = radioTime & 0xFF
            ttiTime = frame*SLOT_PER_FRAME + slot

            self.spinTtiTimeChangeFlag = True
            self.spinFrameSlotChangeFlag = True
            self.spinBox_TtiTime.setValue(ttiTime)
            self.spinBox_Frame.setValue(frame)
            self.spinBox_Slot.setValue(slot)
        self.spinRadioTimeChangeFlag = False

    def chooseFile(self):
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self,"选择文件",self.cwd,"All Files (*);;Text Files (*.txt)")
        if fileName != "":
            self.lineEdit_fileName.setText(fileName)
            self.radioButton_choseFile.setChecked(True)
            self.cwd = os.path.dirname(fileName)

    def chooseDir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self,"选择文件夹",self.cwd)
        if dir != "":
            self.lineEdit_DirName.setText(dir)
            self.radioButton_choseDir.setChecked(True)
            self.cwd = dir

    def drawFile(self, fileName):
        print("draw in")
        DrxFileParser(fileName,self.checkBox_onduration.isChecked(),self.checkBox_Inactivity.isChecked(),self.checkBox_UlReTx.isChecked(),self.checkBox_DlReTx.isChecked(),self.textBrowser_output)
        DrxLeftDataProc(self.textBrowser_output)
        plt.show()
        print("draw out")

    def drawDirFileList(self,dirName):
        print("draw in")
        fileList = os.listdir(dirName)
        for list in fileList:
            path = os.path.join(dirName, list)
            if os.path.isfile(path) and os.path.splitext(path)[1] == ".txt":
                print(path)
                self.textBrowser_output.append(path)
                DrxFileParser(path,self.checkBox_onduration.isChecked(),self.checkBox_Inactivity.isChecked(),self.checkBox_UlReTx.isChecked(),self.checkBox_DlReTx.isChecked(),self.textBrowser_output)
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
                win32api.MessageBox(0, "文件不存在", "警告", win32con.MB_ICONWARNING)
            else:
                print(fileName)
                self.textBrowser_output.append(fileName)
                self.p = Process(target=self.drawFile, args=(fileName,))
                self.p.run()
        elif self.radioButton_choseDir.isChecked():
            if not os.path.exists(dirName):
                win32api.MessageBox(0, "文件夹不存在", "警告", win32con.MB_ICONWARNING)
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
