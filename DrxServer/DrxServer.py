import os, sys
from threading import Thread
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QHeaderView,QTableWidgetItem
from PyQt5.QtCore import Qt

from UDPServer import UDP
from DrxDefine import *
from SendGui import SendGui


qtCreatorFile = "DrxServer.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class DrxServer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.udp = UDP()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sendGui = SendGui(self.udp, self.tableWidget)

        self.pushButton_addItem.clicked.connect(self.test_addItem)
        self.pushButton_checkState.clicked.connect(self.CheckClientState)
        self.pushButton_send.clicked.connect(self.sendMsg)
        self.pushButton_test.clicked.connect(self.test)

        self.StartRecvClient()



    def StartRecvClient(self):
        self.t = Thread(target=self.RecvClientMsg, args=())
        self.t.setDaemon(True)
        self.t.start()

    def RecvClientMsg(self):
        while True:
            data,addr = self.udp.receiveFromServer()
            if data is None:
                break
            ip = addr[0]
            state = "未知"
            countAdd = 0
            if "[Start]" in data:
                state = "在线"
                if "response" not in data:
                    countAdd = 1
            elif "[End]" in data:
                state = "下线"
            pos = data.index("Version")
            version = data[pos+len("Version")+1:]
            print(ip,state,pos,version,countAdd)
            self.ModifyTableItem(ip,version,state,countAdd)

    def test(self):
        items=self.tableWidget.selectedItems()
        if items:
            item=items[0]
            print(item.text(),item.row(),item.column())


            # item.setSelected(True)
            # self.tableWidget.verticalScrollBar().setSliderPosition(row)

    def CheckClientState(self):
        items=self.tableWidget.selectedItems()
        for item in items:
            if item.column() == 0:
                ip = item.text()
                print(ip)
                self.udp.sendToServer(QUERY_DRX_CLIENT_STATE, destIp=ip)

    def InstertTableItem(self,ip,ver,state,count):
        print(("new item:%s,%s,%s,%s")%(ip,ver,state,count))
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        item_id = QTableWidgetItem(ip)
        # item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        item_ver = QTableWidgetItem(ver)  # 我们要求它可以修改，所以使用默认的状态即可
        item_state = QTableWidgetItem(state)
        item_count = QTableWidgetItem(count)
        # item_pos.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        self.tableWidget.setItem(row, 0, item_id)
        self.tableWidget.setItem(row, 1, item_ver)
        self.tableWidget.setItem(row, 2, item_state)
        self.tableWidget.setItem(row, 3, item_count)

    def sendMsg(self):
        self.sendGui.show()


    def test_addItem(self):
        self.InstertTableItem("123", "234", "345", "1")

    def ModifyTableItem(self,ip,ver,state,countAdd):
        items=self.tableWidget.findItems(ip,Qt.MatchExactly)
        if items:
            item_ip = items[0]
            row = item_ip.row()
            item_ver = self.tableWidget.item(row,1)
            item_ver.setText(ver)
            item_state = self.tableWidget.item(row,2)
            item_state.setText(state)
            item_count = self.tableWidget.item(row,3)
            count = int(item_count.text())
            item_count.setText(str(count+countAdd))
            print(("modify:%s,%s,%s,%s")%(item_ip.text(),item_ver.text(),item_state.text(),item_count.text()))
        else:
            self.InstertTableItem(ip,ver,state,"1")

    def closeEvent(self, *args, **kwargs):
        self.udp.close()
        self.sendGui.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DrxServer()
    window.show()
    sys.exit(app.exec_())
