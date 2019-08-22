import sys
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, uic, QtCore

from DrxDefine import VERSION


qtCreatorFile = "About.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class About(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        QtWidgets.QDialog.setWindowFlags(self,QtCore.Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("drxGui.ico"))
        self.setupUi(self)

        self.label_version.setText("Version:" + VERSION)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = About()
    window.show()
    sys.exit(app.exec_())