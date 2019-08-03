import sys,os,time
from PyQt5 import QtWidgets, uic
from DrxProc import DrxFileParser,DrxLeftDataProc,ClearListData
import matplotlib.pyplot as plt
from threading import Thread
from multiprocessing import Process

qtCreatorFile = "DrxGUI.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def draw(fileName):
    print("123")
    # time.sleep(1)
    # plt.close('all')
    DrxFileParser(fileName)
    DrxLeftDataProc()
    plt.show()
    print("456")

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

    def chooseFile(self):
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self,"选择文件",self.cwd,"All Files (*);;Text Files (*.txt)")
        print(fileName)
        self.lineEdit_fileName.setText(fileName)

    def chooseDir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self,"选择文件夹",self.cwd)
        print(dir)
        self.lineEdit_DirName.setText(dir)

    def draw(self,fileName):
        print("123")
        # time.sleep(1)
        # plt.close('all')
        DrxFileParser(fileName)
        DrxLeftDataProc()
        plt.show()
        print("456")

    def drawDrxPlot(self):
        ClearListData()
        fileName = self.lineEdit_fileName.text().strip()
        dirName = self.lineEdit_DirName.text().strip()
        if fileName != "":
            print(fileName)
            # DrxFileParser(fileName)
            # DrxLeftDataProc()
            self.p = Process(target=draw,args=(fileName,))
            self.p.start()
            # plt.show()
        elif os.path.exists(dirName):
            fileList = os.listdir(dirName)
            for list in fileList:
                path = os.path.join(dirName,list)
                if os.path.isfile(path) and os.path.splitext(path)[1] == ".txt":
                    print(path)
                    DrxFileParser(path)
            DrxLeftDataProc()
            plt.show()

    def clearAllFigure(self):
        print("close")
        self.p.terminate()
        print("close 2")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())