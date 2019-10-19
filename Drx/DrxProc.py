import re
import matplotlib.pyplot as plt
from DrxDefine import *

ondurationRegexStr = r"# \[OnDuration\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetOnDurationTimeToShareMem"
ondurationRegexInit = re.compile(ondurationRegexStr)
ondurationRegex = ondurationRegexInit

inActivityRegexStr = r"# \[InActivity\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetInActivityTimeToShareMem"
inActivityRegexInit = re.compile(inActivityRegexStr)
inActivityRegex = inActivityRegexInit

ulRetxRegexStr = r"# \[UlRetx    \] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetUlReTxTimeToShareMem"
ulRetxRegexInit = re.compile(ulRetxRegexStr)
ulRetxRegex = ulRetxRegexInit

dlRetxRegexStr = r"# \[DlRetx    \] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetDlReTxTimeToShareMem"
dlRetxRegexInit = re.compile(dlRetxRegexStr)
dlRetxRegex = dlRetxRegexInit

ondurationList=[('0','0','0','0')]
ondurationTmpList=[('0','0','0','0')]

inactivityList=[('0', '0', '0', '0')]
inactivityTmpList=[('0', '0', '0', '0')]

ulRetxList=[('0', '0', '0', '0')]
ulRetxTmpList=[('0', '0', '0', '0')]

dlRetxList=[('0', '0', '0', '0')]
dlRetxTmpList=[('0', '0', '0', '0')]

def ResetRegex():
    global ondurationRegexInit,ondurationRegex,inActivityRegexInit,inActivityRegex,ulRetxRegexInit,ulRetxRegex,dlRetxRegexInit,dlRetxRegex
    ondurationRegex = ondurationRegexInit
    inActivityRegex = inActivityRegexInit
    ulRetxRegex = ulRetxRegexInit
    dlRetxRegex = dlRetxRegexInit

def UpdateRegexWithUeId(ueId):
    global ondurationRegexStr,ondurationRegex,inActivityRegexStr,inActivityRegex,ulRetxRegexStr,ulRetxRegex,dlRetxRegexStr,dlRetxRegex
    ueIdStr = "ueId:%4d" % (ueId)
    ondurationStr = ueIdStr + ondurationRegexStr
    print(ondurationStr)
    ondurationRegex = re.compile(ondurationStr)

    inActivityStr = ueIdStr + inActivityRegexStr
    print(inActivityStr)
    inActivityRegex = re.compile(inActivityStr)

    ulRetxStr = ueIdStr + ulRetxRegexStr
    print(ulRetxStr)
    ulRetxRegex = re.compile(ulRetxStr)

    dlRetxStr = ueIdStr + dlRetxRegexStr
    print(dlRetxStr)
    dlRetxRegex = re.compile(dlRetxStr)


def ProcFileActivityRange(line,Regex,list,tmpList):
    mo = Regex.search(line)
    if mo != None:
        # print(mo.groups())
        value = mo.groups()
        if int(value[0]) < int(list[-1][0])//2:
            if int(value[0])*20+int(value[1])<int(tmpList[-1][0])*20+int(tmpList[-1][1]):
                tmpList.pop()
            tmpList.append(value)
        elif int(value[0])*20+int(value[1])<20480:
            if int(value[0])*20+int(value[1])<int(list[-1][0])*20+int(list[-1][1]):
                list.pop()
            list.append(value)

def DrawList(type,list,value,activeY,activeValue,ax):
    global ondurationTmpList,inactivityTmpList,ulRetxTmpList,dlRetxTmpList
    if len(list)>1:
        Y = [value]*1024*20
        value_Y = value + 0.1
        activeYValue = activeValue + 0.1
        del list[0]
        for startFrame, startSlot, endFrame, endSlot in list:
            # print(startFrame,startSlot,endFrame,endSlot)
            startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
            endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
            if startIndex > endIndex:
                Y[startIndex:] = [value_Y]*(len(Y)-startIndex)
                activeY[startIndex:] = [activeYValue] * (len(activeY) - startIndex)
                if type == "Onduration":
                    ondurationTmpList.insert(1, ('0','0',endFrame,endSlot))
                if type == "InActivity":
                    inactivityTmpList.insert(1, ('0', '0', endFrame, endSlot))
                if type == "UlRetx":
                    ulRetxTmpList.insert(1, ('0', '0', endFrame, endSlot))
                if type == "DlRetx":
                    dlRetxTmpList.insert(1, ('0', '0', endFrame, endSlot))
            else:
                Y[startIndex:endIndex+1] = [value_Y]*(endIndex+1-startIndex)
                activeY[startIndex:endIndex+1] = [activeYValue]*(endIndex+1-startIndex)
        ax.plot(Y,linewidth=0.5, label=type)

def Draw(list1, value1, list2, value2, list3, value3,list4,value4,value):
    if len(list1)<=1 and len(list2)<=1 and len(list3)<=1 and len(list4)<=1:
        return

    fig = plt.figure(frameon = True)
    ax = fig.subplots()

    activeY = [value]*1024*20

    DrawList("Onduration",list1,value1,activeY,value, ax)
    DrawList("InActivity", list2, value2, activeY, value, ax)
    DrawList("UlRetx", list3, value3, activeY, value, ax)
    DrawList("DlRetx", list4, value4, activeY, value, ax)

    ax.plot(activeY, linewidth=0.5, label="Active")
    ax.set_ylim(0,1.1)
    ax.set(xlabel='TTI time (0~20479)', ylabel='active type', title='DRX')
    ax.legend(loc='upper left', shadow=True, fontsize='medium')


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

def printList(textBrowser_output):
    global ondurationList,inactivityList,ulRetxList,dlRetxList
    print("onduration:", ondurationList)
    print("inactivity:", inactivityList)
    print("ulretx    :", ulRetxList)
    print("dlretx    :", dlRetxList)
    if textBrowser_output != None:
        textBrowser_output.append("onduration:" + str(ondurationList))
        textBrowser_output.append("inactivity:" + str(inactivityList))
        textBrowser_output.append("ulretx    :" + str(ulRetxList))
        textBrowser_output.append("dlretx    :" + str(dlRetxList))

def printTmpList(textBrowser_output):
    global ondurationTmpList,inactivityTmpList,ulRetxTmpList,dlRetxTmpList
    print("ondurationTmp:", ondurationTmpList)
    print("inactivityTmp:", inactivityTmpList)
    print("ulretxTmp    :", ulRetxTmpList)
    print("dlretxTmp    :", dlRetxTmpList)
    if textBrowser_output != None:
        textBrowser_output.append("ondurationTmp:" + str(ondurationTmpList))
        textBrowser_output.append("inactivityTmp:" + str(inactivityTmpList))
        textBrowser_output.append("ulretxTmp    :" + str(ulRetxTmpList))
        textBrowser_output.append("dlretxTmp    :" + str(dlRetxTmpList))

def DrxFileParser(fileName,isDrawOnduration,isDrawInactivity,isDrawUlRetx,isDrawDlRetx,textBrowser_output):
    global ondurationList,ondurationTmpList,inactivityList,inactivityTmpList,ulRetxList,ulRetxTmpList,dlRetxList,dlRetxTmpList
    with open(fileName, encoding='UTF-8') as drxFile:
        for line in drxFile:
            if isDrawOnduration:
                ProcFileActivityRange(line,ondurationRegex,ondurationList,ondurationTmpList)
            if isDrawInactivity:
                ProcFileActivityRange(line, inActivityRegex, inactivityList, inactivityTmpList)
            if isDrawUlRetx:
                ProcFileActivityRange(line,ulRetxRegex,ulRetxList,ulRetxTmpList)
            if isDrawDlRetx:
                ProcFileActivityRange(line,dlRetxRegex,dlRetxList,dlRetxTmpList)

            if len(ondurationTmpList) > 8 or len(inactivityTmpList) > 8 or len(ulRetxTmpList) > 8 or len(dlRetxTmpList) > 8:
                printList(textBrowser_output)
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
    printList(textBrowser_output)
    Draw(ondurationList, ONDURATION_VALUE, inactivityList, INACTIVITY_VALUE,ulRetxList,ULRETX_VALUE,dlRetxList,DLRETX_VALUE,ACTIVE_VALUE)
    printTmpList(textBrowser_output)
    Draw(ondurationTmpList, ONDURATION_VALUE, inactivityTmpList, INACTIVITY_VALUE,ulRetxTmpList,ULRETX_VALUE,dlRetxTmpList,DLRETX_VALUE,ACTIVE_VALUE)

if __name__ == "__main__":
    # fileName = "log.txt"
    fileName = "Python打包exe.txt"
    DrxFileParser(fileName,True,True,True,True,None)
    DrxLeftDataProc(None)
    plt.show()



