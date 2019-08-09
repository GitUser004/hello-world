import re
import matplotlib.pyplot as plt
from DrxDefine import *


ondurationRegexStr = r"\[OnDuration\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetOnDurationTimeToShareMem"
ondurationRegex = re.compile(ondurationRegexStr)

inActivityRegexStr = r"\[InActivity\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetInActivityTimeToShareMem"
inActivityRegex = re.compile(inActivityRegexStr)

ulRetxRegexStr = r"\[UlRetx    \] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetUlReTxTimeToShareMem"
ulRetxRegex = re.compile(ulRetxRegexStr)

dlRetxRegexStr = r"\[DlRetx    \] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetDlReTxTimeToShareMem"
dlRetxRegex = re.compile(dlRetxRegexStr)

ondurationList=[('0','0','0','0')]
ondurationTmpList=[('0','0','0','0')]

inactivityList=[('0', '0', '0', '0')]
inactivityTmpList=[('0', '0', '0', '0')]

ulRetxList=[('0', '0', '0', '0')]
ulRetxTmpList=[('0', '0', '0', '0')]

dlRetxList=[('0', '0', '0', '0')]
dlRetxTmpList=[('0', '0', '0', '0')]


def ProcOnduration(line):
    global ondurationList,ondurationTmpList
    mo = ondurationRegex.search(line)
    if mo != None:
        # print(mo.groups())
        value = mo.groups()
        if int(value[0]) < int(ondurationList[-1][0])//2:
            if int(value[0])*20+int(value[1])<int(ondurationTmpList[-1][0])*20+int(ondurationTmpList[-1][1]):
                ondurationTmpList.pop()
            ondurationTmpList.append(value)
        elif int(value[0])*20+int(value[1])<20480:
            if int(value[0])*20+int(value[1])<int(ondurationList[-1][0])*20+int(ondurationList[-1][1]):
                ondurationList.pop()
            ondurationList.append(value)

def ProcInactivity(line):
    global inactivityList,inactivityTmpList
    mo = inActivityRegex.search(line)
    if mo != None:
        # print(mo.groups())
        value = mo.groups()
        if int(value[0]) < int(inactivityList[-1][0])//2:
            if int(value[0])*20+int(value[1])<int(inactivityTmpList[-1][0])*20+int(inactivityTmpList[-1][1]):
                inactivityTmpList.pop()
            inactivityTmpList.append(value)
        elif int(value[0])*20+int(value[1])<20480:
            if int(value[0])*20+int(value[1])<int(inactivityList[-1][0])*20+int(inactivityList[-1][1]):
                inactivityList.pop()
            inactivityList.append(value)

def ProcUlRetx(line):
    global ulRetxList, ulRetxTmpList
    mo = ulRetxRegex.search(line)
    if mo != None:
        # print(mo.groups())
        value = mo.groups()
        if int(value[0]) < int(ulRetxList[-1][0]) // 2:
            if int(value[0]) * 20 + int(value[1]) < int(ulRetxTmpList[-1][0]) * 20 + int(ulRetxTmpList[-1][1]):
                ulRetxTmpList.pop()
            ulRetxTmpList.append(value)
        elif int(value[0]) * 20 + int(value[1]) < 20480:
            if int(value[0]) * 20 + int(value[1]) < int(ulRetxList[-1][0]) * 20 + int(ulRetxList[-1][1]):
                ulRetxList.pop()
            ulRetxList.append(value)

def ProcDlRetx(line):
    global dlRetxList, dlRetxTmpList
    mo = dlRetxRegex.search(line)
    if mo != None:
        # print(mo.groups())
        value = mo.groups()
        if int(value[0]) < int(dlRetxList[-1][0]) // 2:
            if int(value[0]) * 20 + int(value[1]) < int(dlRetxTmpList[-1][0]) * 20 + int(dlRetxTmpList[-1][1]):
                dlRetxTmpList.pop()
            dlRetxTmpList.append(value)
        elif int(value[0]) * 20 + int(value[1]) < 20480:
            if int(value[0]) * 20 + int(value[1]) < int(dlRetxList[-1][0]) * 20 + int(dlRetxList[-1][1]):
                dlRetxList.pop()
            dlRetxList.append(value)

def DrawList(type,list,value,activeY,activeValue,ax):
    if len(list)>1:
        Y = [value]*1024*20
        value_1 = value + 0.1
        activeYValue = activeValue + 0.1
        del list[0]
        for startFrame, startSlot, endFrame, endSlot in list:
            # print(startFrame,startSlot,endFrame,endSlot)
            startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
            endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
            Y[startIndex:endIndex+1] = [value_1]*(endIndex+1-startIndex)
            activeY[startIndex:endIndex+1] = [activeYValue]*(endIndex+1-startIndex)
        line = ax.plot(Y,linewidth=0.5, label=type)
        legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')
        # line = ax.plot(Y,'o',linewidth=0.5,label="Onduration",markersize = 1)
        # plt.setp(line, linewidth=4)

def Draw(list1, value1, list2, value2, list3, value3,list4,value4,value):
    if len(list1)<=1 and len(list2)<=1 and len(list3)<=1 and len(list4)<=1:
        return

    fig = plt.figure(frameon = True)
    ax = fig.subplots()

    activeY = [value]*1024*20
    value_1 = value + 0.1

    DrawList("Onduration",list1,value1,activeY,value,ax)
    DrawList("InActivity", list1, value1, activeY, value, ax)

    # if len(list1)>1:
    #     Y = [value1]*1024*20
    #     value1_1 = value1 + 0.1
    #     del list1[0]
    #     for startFrame, startSlot, endFrame, endSlot in list1:
    #         # print(startFrame,startSlot,endFrame,endSlot)
    #         startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
    #         endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
    #         Y[startIndex:endIndex+1] = [value1_1]*(endIndex+1-startIndex)
    #         activeY[startIndex:endIndex+1] = [value_1]*(endIndex+1-startIndex)
    #     line = ax.plot(Y,linewidth=0.5, label="Onduration")
    #     legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')
    #     # line = ax.plot(Y,'o',linewidth=0.5,label="Onduration",markersize = 1)
    #     # plt.setp(line, linewidth=4)

    if len(list2)>1:
        Y = [value2]*1024*20
        value2_2 = value2 + 0.1
        del list2[0]
        for startFrame, startSlot, endFrame, endSlot in list2:
            # print(startFrame,startSlot,endFrame,endSlot)
            startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
            endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
            Y[startIndex:endIndex+1] = [value2_2]*(endIndex+1-startIndex)
            activeY[startIndex:endIndex+1] = [value_1]*(endIndex+1-startIndex)
        line = ax.plot(Y,linewidth=0.5,label="InActivity")
        legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')

    if len(list3)>1:
        Y = [value3]*1024*20
        value3_3 = value3 + 0.1
        del list3[0]
        for startFrame, startSlot, endFrame, endSlot in list3:
            # print(startFrame,startSlot,endFrame,endSlot)
            startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
            endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
            Y[startIndex:endIndex+1] = [value3_3]*(endIndex+1-startIndex)
            activeY[startIndex:endIndex+1] = [value_1]*(endIndex+1-startIndex)
        line = ax.plot(Y,linewidth=0.5,label="UlRetx")
        legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')

    if len(list4)>1:
        Y = [value4]*1024*20
        value4_4 = value4 + 0.1
        del list4[0]
        for startFrame, startSlot, endFrame, endSlot in list4:
            # print(startFrame,startSlot,endFrame,endSlot)
            startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
            endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
            Y[startIndex:endIndex+1] = [value4_4]*(endIndex+1-startIndex)
            activeY[startIndex:endIndex+1] = [value_1]*(endIndex+1-startIndex)
        line = ax.plot(Y,linewidth=0.5,label="DlRetx")
        legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')

    line = ax.plot(activeY, linewidth=0.5, label="Active")
    legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')


def ClearListData():
    global ondurationTmpList,ondurationList,inactivityTmpList,inactivityList,ulRetxList,ulRetxTmpList,dlRetxList,dlRetxTmpList
    ondurationList = [('0', '0', '0', '0')]
    ondurationTmpList = [('0', '0', '0', '0')]

    inactivityList = [('0', '0', '0', '0')]
    inactivityTmpList = [('0', '0', '0', '0')]

    ulRetxList = [('0', '0', '0', '0')]
    ulRetxTmpList = [('0', '0', '0', '0')]

    dlRetxList = [('0', '0', '0', '0')]
    dlRetxTmpList = [('0', '0', '0', '0')]

def DrxFileParser(fileName,isDrawOnduration,isDrawInactivity,isDrawUlRetx,isDrawDlRetx,textBrowser_output):
    global ondurationList,ondurationTmpList,inactivityList,inactivityTmpList,ulRetxList,ulRetxTmpList,dlRetxList,dlRetxTmpList
    with open(fileName) as drxFile:
        for line in drxFile:
            if isDrawOnduration:
                ProcOnduration(line)
            if isDrawInactivity:
                ProcInactivity(line)
            if isDrawUlRetx:
                ProcUlRetx(line)
            if isDrawDlRetx:
                ProcDlRetx(line)

            if len(ondurationTmpList) > 8 or len(inactivityTmpList) > 8 or len(ulRetxTmpList) > 8 or len(dlRetxTmpList) > 8:
                print("onduration:",ondurationList)
                print("inactivity:",inactivityList)
                print("ulretx    :",ulRetxList)
                print("dlretx    :",dlRetxList)
                if textBrowser_output != None:
                    textBrowser_output.append("onduration:"+str(ondurationList))
                    textBrowser_output.append("inactivity:" + str(inactivityList))
                    textBrowser_output.append("ulretx    :" + str(ulRetxList))
                    textBrowser_output.append("dlretx    :" + str(dlRetxList))
                Draw(ondurationList, ONDURATION_VALUE, inactivityList, INACTIVITY_VALUE,ulRetxList,ULRETX_VALUE,dlRetxList,DLRETX_VALUE,ACTIVE_VALUE)
                ondurationList = ondurationTmpList
                ondurationTmpList = [('0', '0', '0', '0')]
                inactivityList = inactivityTmpList
                inactivityTmpList = [('0', '0', '0', '0')]
                ulRetxList = ulRetxTmpList
                ulRetxTmpList = [('0', '0', '0', '0')]
                dlRetxList = dlRetxTmpList
                dlRetxTmpList = [('0', '0', '0', '0')]

def DrxLeftDataProc(textBrowser_output):
    global ondurationList,ondurationTmpList,inactivityList,inactivityTmpList,ulRetxList,ulRetxTmpList,dlRetxList,dlRetxTmpList
    print("onduration:", ondurationList)
    print("inactivity:", inactivityList)
    print("ulretx    :", ulRetxList)
    print("dlretx    :", dlRetxList)
    if textBrowser_output != None:
        textBrowser_output.append("onduration:" + str(ondurationList))
        textBrowser_output.append("inactivity:" + str(inactivityList))
        textBrowser_output.append("ulretx    :" + str(ulRetxList))
        textBrowser_output.append("dlretx    :" + str(dlRetxList))
    Draw(ondurationList, ONDURATION_VALUE, inactivityList, INACTIVITY_VALUE,ulRetxList,ULRETX_VALUE,dlRetxList,DLRETX_VALUE,ACTIVE_VALUE)
    print("ondurationTmp:", ondurationTmpList)
    print("inactivityTmp:", inactivityTmpList)
    print("ulretxTmp    :", ulRetxTmpList)
    print("dlretxTmp    :", dlRetxTmpList)
    if textBrowser_output != None:
        textBrowser_output.append("ondurationTmp:" + str(ondurationTmpList))
        textBrowser_output.append("inactivityTmp:" + str(inactivityTmpList))
        textBrowser_output.append("ulretxTmp    :" + str(ulRetxTmpList))
        textBrowser_output.append("dlretxTmp    :" + str(dlRetxTmpList))
    Draw(ondurationTmpList, ONDURATION_VALUE, inactivityTmpList, INACTIVITY_VALUE,ulRetxTmpList,ULRETX_VALUE,dlRetxTmpList,DLRETX_VALUE,ACTIVE_VALUE)

if __name__ == "__main__":
    fileName = "log.txt"
    DrxFileParser(fileName,True,False,False,True,None)
    DrxLeftDataProc(None)
    plt.show()



