import re
import matplotlib.pyplot as plt
from DrxDefine import *

ondurationRegexStr = r"\[OnDuration\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetOnDurationTimeToShareMem"
ondurationRegex = re.compile(ondurationRegexStr)

inActivityRegexStr = r"\[InActivity\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetInActivityTimeToShareMem"
inActivityRegex = re.compile(inActivityRegexStr)

ondurationList=[('0','0','0','0')]
ondurationTmpList=[('0','0','0','0')]

inactivityList=[('0', '0', '0', '0')]
inactivityTmpList=[('0', '0', '0', '0')]


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
        if int(value[0]) < int(ondurationList[-1][0])//2:
            if int(value[0])*20+int(value[1])<int(inactivityTmpList[-1][0])*20+int(inactivityTmpList[-1][1]):
                inactivityTmpList.pop()
            inactivityTmpList.append(value)
        elif int(value[0])*20+int(value[1])<20480:
            if int(value[0])*20+int(value[1])<int(inactivityList[-1][0])*20+int(inactivityList[-1][1]):
                inactivityList.pop()
            inactivityList.append(value)

def Draw(list1, value1, list2, value2):
    if len(list1)<=1 and len(list2)<=1:
        return

    fig = plt.figure(frameon = True)
    ax = fig.subplots()

    if len(list1)>1:
        Y = [0]*1024*20
        del list1[0]
        for startFrame, startSlot, endFrame, endSlot in list1:
            # print(startFrame,startSlot,endFrame,endSlot)
            startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
            endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
            Y[startIndex:endIndex+1] = [value1]*(endIndex+1-startIndex)
            ax.plot(Y)

    if len(list2)>1:
        Y = [0]*1024*20
        del list2[0]
        for startFrame, startSlot, endFrame, endSlot in list2:
            # print(startFrame,startSlot,endFrame,endSlot)
            startIndex = int(startFrame) * SLOT_PER_FRAME + int(startSlot)
            endIndex = int(endFrame) * SLOT_PER_FRAME + int(endSlot)
            Y[startIndex:endIndex+1] = [value2]*(endIndex+1-startIndex)
            ax.plot(Y)

def ClearListData():
    global ondurationTmpList,ondurationList,inactivityTmpList,inactivityList
    ondurationList = [('0', '0', '0', '0')]
    ondurationTmpList = [('0', '0', '0', '0')]

    inactivityList = [('0', '0', '0', '0')]
    inactivityTmpList = [('0', '0', '0', '0')]

def DrxFileParser(fileName):
    global ondurationList,ondurationTmpList,inactivityList,inactivityTmpList
    with open(fileName) as drxFile:
        for line in drxFile:
            ProcOnduration(line)
            ProcInactivity(line)
            if len(ondurationTmpList) > 9 and len(inactivityTmpList) > 9:
                print(ondurationList)
                print(inactivityList)
                Draw(ondurationList, ONDURATION_VALUE, inactivityList, INACTIVITY_VALUE)
                ondurationList = ondurationTmpList
                ondurationTmpList = [('0', '0', '0', '0')]
                inactivityList = inactivityTmpList
                inactivityTmpList = [('0', '0', '0', '0')]

def DrxLeftDataProc():
    global ondurationList,ondurationTmpList,inactivityList,inactivityTmpList
    print(ondurationList)
    print(inactivityList)
    Draw(ondurationList, ONDURATION_VALUE, inactivityList, INACTIVITY_VALUE)
    print(ondurationTmpList)
    print(inactivityTmpList)
    Draw(ondurationTmpList, ONDURATION_VALUE, inactivityTmpList, INACTIVITY_VALUE)

if __name__ == "__main__":
    fileName = "log.txt"
    DrxFileParser(fileName)
    DrxLeftDataProc()
    plt.show()



