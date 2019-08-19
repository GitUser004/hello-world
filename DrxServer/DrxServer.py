import os, sys
import matplotlib.pyplot as plt
from multiprocessing import Process
from threading import Thread
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QHeaderView,QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
import win32api, win32con
from PyQt5.QtCore import Qt

from UDP import UDP


qtCreatorFile = "DrxServer.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class DrxServer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.udp = UDP()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pushButton_start.clicked.connect(self.StartRecvClient)

    def StartRecvClient(self):
        self.t = Thread(target=self.RecvClientMsg, args=())
        self.t.start()

    def RecvClientMsg(self):

        ip = "10.4.211.37"
        print(ip)
        # newItem = QTableWidgetItem(ip)
        # self.tableWidget.setItem(0, 0, newItem)

        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        item_id = QTableWidgetItem(ip)
        # item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        item_ver = QTableWidgetItem("door")  # 我们要求它可以修改，所以使用默认的状态即可
        item_status = QTableWidgetItem("(1,2)")
        # item_pos.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择

        self.tableWidget.setItem(row, 0, item_id)
        self.tableWidget.setItem(row, 1, item_ver)
        self.tableWidget.setItem(row, 2, item_status)

        # while True:
        #     data,addr = self.udp.receiveFromServer()
        #     if data is None:
        #         break
        #     print(data,addr)
        #     ip = addr[0]
        #     newItem = QTableWidgetItem(ip)
        #     self.tableWidget.setItem(0,0,newItem)



    def closeEvent(self, *args, **kwargs):
        self.udp.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DrxServer()
    window.show()
    sys.exit(app.exec_())
