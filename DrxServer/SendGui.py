import sys
from PyQt5 import QtWidgets, uic, QtCore


qtCreatorFile = "send.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class SendGui(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self, udp, tableWidget):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        QtWidgets.QDialog.setWindowFlags(self, QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        self.udp = udp
        self.tableWidget = tableWidget

        self.pushButton_send.clicked.connect(self.send)

    def send(self):
        text = self.plainTextEdit_send.toPlainText().strip()
        if text:
            items = self.tableWidget.selectedItems()
            for item in items:
                if item.column() == 0:
                    ip = item.text()
                    print(text, ip)
                    self.udp.sendToServer(text, destIp=ip)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SendGui()
    window.show()
    sys.exit(app.exec_())