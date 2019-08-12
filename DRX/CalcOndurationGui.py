import sys
from PyQt5 import QtWidgets, uic, QtCore

LongCycle = ['10','20','30','40']
ShortCycle = ['10','20','30','40']
OndurationTimer = ['10','20','30','40']


qtCreatorFile = "CalcOnduration.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class OndurationGui(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        QtWidgets.QDialog.setWindowFlags(self,QtCore.Qt.WindowCloseButtonHint)

        self.comboBox_longCycle.addItems(LongCycle)
        self.comboBox_shortCycle.addItems(ShortCycle)
        self.comboBox_ondurationTimer.addItems(OndurationTimer)

        self.pushButton_calc.clicked.connect(self.CalcOndurationRange)


    def CalcOndurationRange(self):
        longCycle = int(self.comboBox_longCycle.currentText())
        shortCycle = int(self.comboBox_shortCycle.currentText())
        ondurationTimer = int(self.comboBox_ondurationTimer.currentText())
        startOgset = self.spinBox_StartOffset.value()
        slotOffset = self.spinBox_SlotOffset.value()

        frame = self.spinBox_frame.value()
        slot = self.spinBox_slot.value()

        print("long:%d short %d onduration %d startOfsset %d slotOffset %d frame %d slot %d" %(longCycle,shortCycle,ondurationTimer,startOgset,slotOffset,frame,slot))

        # self.textBrowser_outpt.setText()

        pass




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OndurationGui()
    window.show()
    sys.exit(app.exec_())