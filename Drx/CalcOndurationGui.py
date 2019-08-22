import sys
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, uic, QtCore

from DrxDefine import SLOT_PER_FRAME,SLOT_PER_SUBFRAME,MAX_SUBFRAME_PER_FRAME,MAX_SUBFRAME,MAX_TTI_TIME

LongCycle = ['10','20','32','40','60', '64', '70', '80', '128','160','256','320','512', '640', '1024','1280','2048','2560','5120', '10240']
ShortCycle = ['2','3','4','5', '6', '7', '8', '10','14','16','20','30','32','35','40', '64', '80','128','160','256','320','512', '640']
OndurationTimer = ['1','2','3','4','5', '6', '8', '10','20','30','40','50', '60', '80', '100','200','300','400','500', '600', '800', '1000','1200','1600']

qtCreatorFile = "CalcOnduration.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class OndurationGui(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setWindowIcon(QIcon("drxGui.ico"))
        QtWidgets.QDialog.setWindowFlags(self,QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        self.comboBox_longCycle.addItems(LongCycle)
        self.comboBox_shortCycle.addItems(ShortCycle)
        self.comboBox_ondurationTimer.addItems(OndurationTimer)

        self.pushButton_calc.clicked.connect(self.CalcOndurationRange)

    def CheckPara(self):
        if self.longCycle <= self.ondurationTimer:
            self.textBrowser_outpt.setText("参数不满足约束：LongCycle > OndurationTimer")
            return False
        if self.longCycle <= self.startOffset:
            self.textBrowser_outpt.setText("参数不满足约束：LongCycle > StartOffset")
            return False
        if self.longCycle < self.shortCycle:
            self.textBrowser_outpt.setText("参数不满足约束：LongCycle >= ShortCycle")
            return False
        if self.longCycle % self.shortCycle != 0:
            self.textBrowser_outpt.setText("参数不满足约束：LongCycle % ShortCycle == 0")
            return False
        if self.shortCycle <= self.ondurationTimer:
            self.textBrowser_outpt.setText("参数不满足约束：ShortCycle > OndurationTimer")
            return False
        return True

    def CalcOndurationRange(self):
        self.longCycle = int(self.comboBox_longCycle.currentText())
        self.shortCycle = int(self.comboBox_shortCycle.currentText())
        self.ondurationTimer = int(self.comboBox_ondurationTimer.currentText())
        self.startOffset = self.spinBox_StartOffset.value()
        self.slotOffset = self.spinBox_SlotOffset.value() // 16

        self.currentframe = self.spinBox_frame.value()
        self.currentslot = self.spinBox_slot.value()
        self.currentSubFrame = self.currentslot // SLOT_PER_SUBFRAME

        print("long:%d short %d onduration %d startOfsset %d slotOffset %d frame %d slot %d" % (self.longCycle, self.shortCycle, self.ondurationTimer, self.startOffset, self.slotOffset, self.currentframe, self.currentslot))
        res = self.CheckPara()
        if not res:
            return

        startTti,endTti = self.CalcOndurationStartEndTime(self.longCycle,self.ondurationTimer, self.startOffset)
        str = ("long  cycle [frame|slot] : [%2d|%2d] -> [%2d|%2d]") % (startTti//SLOT_PER_FRAME,startTti%SLOT_PER_FRAME,endTti//SLOT_PER_FRAME,endTti%SLOT_PER_FRAME)
        self.textBrowser_outpt.setText(str)

        startTti,endTti = self.CalcOndurationStartEndTime(self.shortCycle,self.ondurationTimer, self.startOffset % self.shortCycle)
        str = ("short cycle [frame|slot] : [%2d|%2d] -> [%2d|%2d]") % (startTti//SLOT_PER_FRAME,startTti%SLOT_PER_FRAME,endTti//SLOT_PER_FRAME,endTti%SLOT_PER_FRAME)
        self.textBrowser_outpt.append(str)


    def TtiTimeAdd(self, base, diffTtiTime):
        return (base + MAX_TTI_TIME + diffTtiTime) % MAX_TTI_TIME

    def CalcOndurationStartEndTime(self,cycle,ondurationTimer,startOffset):
        reverseFlag = False
        curSubFrame = self.currentframe * MAX_SUBFRAME_PER_FRAME + self.currentSubFrame
        curModuloValue = curSubFrame % cycle
        deltaSubFrameFromCur = startOffset - curModuloValue + (cycle if (startOffset < curModuloValue) else 0)
        startSubFrame = (curSubFrame + deltaSubFrameFromCur) % MAX_SUBFRAME
        if curSubFrame > startSubFrame:   #发生了反转
            print("CurrTime:[%4d|%2d] # [OnDuration] -CalcOndurationStartEndTime reverse curSubFrame=%d,startSubFrame=%d" %(self.currentframe, self.currentslot,curSubFrame,startSubFrame))
            reverseFlag = True
            startSubFrame = startOffset
        startTti = startSubFrame * SLOT_PER_SUBFRAME + self.slotOffset
        endTti = self.TtiTimeAdd(startTti, ondurationTimer * SLOT_PER_SUBFRAME -1)

        timeRange = self.JudgeCurTimeInOndurationRange(reverseFlag, startTti, endTti, cycle)

        return timeRange



    def JudgeCurTimeInOndurationRange(self, reverseFlag, startTti, endTti, cycle):
        if ((not reverseFlag) and self.IsRadioTimeRangeIn(startTti, endTti, self.TtiTimeAdd(self.currentframe * SLOT_PER_FRAME + self.currentslot, cycle * SLOT_PER_SUBFRAME))):
            startTti = self.TtiTimeAdd(startTti, -(cycle * SLOT_PER_SUBFRAME))
            endTti = self.TtiTimeAdd(endTti, -(cycle * SLOT_PER_SUBFRAME))
        return (startTti, endTti)

    def IsRadioTimeRangeIn(self,ttiBegin,ttiEnd,ttiCur):
        if ttiBegin <= ttiEnd:
            return (ttiBegin <= ttiCur) and (ttiCur <= ttiEnd)
        else:
            return ((ttiBegin <= ttiCur) and (ttiCur <= (ttiEnd + MAX_TTI_TIME))) or ((ttiBegin <= (ttiCur + MAX_TTI_TIME)) and ((ttiCur + MAX_TTI_TIME) <= (ttiEnd + MAX_TTI_TIME)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OndurationGui()
    window.show()
    sys.exit(app.exec_())