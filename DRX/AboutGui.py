import sys
from PyQt5 import QtWidgets, uic, QtCore


qtCreatorFile = "About.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class About(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        QtWidgets.QDialog.setWindowFlags(self,QtCore.Qt.WindowCloseButtonHint)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = About()
    window.show()
    sys.exit(app.exec_())