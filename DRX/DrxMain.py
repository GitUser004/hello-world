import os,sys
from multiprocessing import Process
import matplotlib.pyplot as plt
from DrxProc import DrxFileParser, DrxLeftDataProc, ClearListData
from PyQt5 import QtWidgets, uic

qtCreatorFile = "DrxGUI.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.cwd = os.getcwd()

        self.setupUi(self)
        self.pushButton_chooseFile.clicked.connect(self.chooseFile)
        self.pushButton_chooseDir.clicked.connect(self.chooseDir)
        self.pushButton_draw.clicked.connect(self.drawDrxPlot)
        self.pushButton_draw_clear.clicked.connect(self.clearAllFigure)
        self.pushButton_test.clicked.connect(self.test)

    def test(self):
        a=self.checkBox_onduration.isChecked()
        print(a)

    def chooseFile(self):
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self,"选择文件",self.cwd,"All Files (*);;Text Files (*.txt)")
        print(fileName)
        if fileName != "":
            self.lineEdit_fileName.setText(fileName)
            self.radioButton_choseFile.setChecked(True)

    def chooseDir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self,"选择文件夹",self.cwd)
        print(dir)
        if dir != "":
            self.lineEdit_DirName.setText(dir)
            self.radioButton_choseDir.setChecked(True)

    def drawFile(self, fileName):
        print("draw in")
        DrxFileParser(fileName,self.checkBox_onduration.isChecked(),self.checkBox_Inactivity.isChecked())
        DrxLeftDataProc(self.checkBox_onduration.isChecked(),self.checkBox_Inactivity.isChecked())
        plt.show()
        print("draw out")

    def drawDirFileList(self,dirName):
        print("draw in")
        fileList = os.listdir(dirName)
        for list in fileList:
            path = os.path.join(dirName, list)
            if os.path.isfile(path) and os.path.splitext(path)[1] == ".txt":
                print(path)
                DrxFileParser(path,self.checkBox_onduration.isChecked(),self.checkBox_Inactivity.isChecked())
        DrxLeftDataProc(self.checkBox_onduration.isChecked(),self.checkBox_Inactivity.isChecked())
        plt.show()
        print("draw out")

    def drawDrxPlot(self):
        ClearListData()
        plt.close('all')
        fileName = self.lineEdit_fileName.text().strip()
        dirName = self.lineEdit_DirName.text().strip()
        if fileName != "" and self.radioButton_choseFile.isChecked():
            print(fileName)
            self.p = Process(target=self.drawFile, args=(fileName,))
            self.p.run()
        elif os.path.exists(dirName) and self.radioButton_choseDir.isChecked():
            print(dirName)
            self.p = Process(target=self.drawDirFileList, args=(dirName,))
            self.p.run()

    def clearAllFigure(self):
        print("close start")
        plt.close('all')
        print("close end")

    # 界面退出时执行
    def closeEvent(self, *args, **kwargs):
        self.clearAllFigure()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
