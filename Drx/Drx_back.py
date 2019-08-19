import re
from matplotlib import pyplot
from itertools import islice
import DrxDefine

ondurationRegexStr = r"\[OnDuration\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetOnDurationTimeToShareMem"
ondurationRegex = re.compile(ondurationRegexStr)

inActivityRegexStr = r"\[InActivity\] AirTime\[\D*(\d+)\|\D*(\d+)\]->\[\D*(\d+)\|\D*(\d+)\]SetInActivityTimeToShareMem"
inActivityRegex = re.compile(inActivityRegexStr)

xAxis = list(range(0, 1024 * DrxDefine.SLOT_PER_FRAME))
activeList = [0]*1024*DrxDefine.SLOT_PER_FRAME
ondurationList = [0]*1024*DrxDefine.SLOT_PER_FRAME
inActivityList = [0]*1024*DrxDefine.SLOT_PER_FRAME

ondurationTmpList = [0] * 500*DrxDefine.SLOT_PER_FRAME


lastOndurationStartIndex = 1023 * 20 + 31
lastOndurationEndIndex = 1023 * 20 + 31
lastInactivityStartIndex = 1023 * 20 + 31
lastInactivityEndIndex = 1023 * 20 + 31

def ProcOnduration(line):
    global lastOndurationEndIndex,lastOndurationStartIndex
    global ondurationList
    mo = ondurationRegex.search(line)
    if mo != None:
        # print(mo.groups())
        startFrame, startSlot, endFrame, endSlot = mo.groups()
        startIndex = int(startFrame) * DrxDefine.SLOT_PER_FRAME + int(startSlot)
        endIndex = int(endFrame) * DrxDefine.SLOT_PER_FRAME + int(endSlot)

        if lastOndurationStartIndex < 20480 and lastOndurationEndIndex < 20480:
            if lastOndurationStartIndex < startIndex or (lastOndurationStartIndex > startIndex and lastOndurationStartIndex - startIndex > 10240):
                print("[%d|%d],[%d|%d]"%(lastOndurationStartIndex/20,lastOndurationStartIndex%20,lastOndurationEndIndex/20,lastOndurationEndIndex%20))
                ondurationList[lastOndurationStartIndex: lastOndurationEndIndex + 1] = [DrxDefine.ONDURATION_VALUE] * (lastOndurationEndIndex + 1 - lastOndurationStartIndex)
                activeList[lastOndurationStartIndex: lastOndurationEndIndex + 1] = [DrxDefine.ACTIVE_VALUE] * (lastOndurationEndIndex + 1 - lastOndurationStartIndex)

        lastOndurationStartIndex = startIndex
        lastOndurationEndIndex = endIndex

def ProcInactivity(line):
    global lastInactivityStartIndex,lastInactivityEndIndex
    global inActivityList
    mo = inActivityRegex.search(line)
    if mo != None:
        # print(mo.groups())
        startFrame, startSlot, endFrame, endSlot = mo.groups()
        startIndex = int(startFrame) * DrxDefine.SLOT_PER_FRAME + int(startSlot)
        endIndex = int(endFrame) * DrxDefine.SLOT_PER_FRAME + int(endSlot)

        if lastInactivityStartIndex < 20480 and lastInactivityEndIndex < 20480:
            if lastInactivityStartIndex < startIndex:
                inActivityList[lastInactivityStartIndex: lastInactivityEndIndex + 1] = [DrxDefine.INACTIVITY_VALUE] * (lastInactivityEndIndex + 1 - lastInactivityStartIndex)
                activeList[lastInactivityStartIndex: lastInactivityEndIndex + 1] = [DrxDefine.ACTIVE_VALUE] * (lastInactivityEndIndex + 1 - lastInactivityStartIndex)

        lastInactivityStartIndex = startIndex
        lastInactivityEndIndex = endIndex

def draw(x):
    pyplot.figure()
    xLabel = ["[" + str(a // 20) + "|" + str(a % 20) + "]" for a in x[0::800]]
    # print(xLabel[:40])
    pyplot.xticks(x[0::800], xLabel, rotation=40)

    # pyplot.scatter(x, ondurationList, s=1)
    # pyplot.scatter(x, inActivityList, s=1)
    # pyplot.figure()
    # pyplot.scatter(x, activeList, s=1)

    pyplot.plot(ondurationList)
    pyplot.show()

def draw2(x):
    fig, ax = pyplot.subplots()
    xticks = list(range(0,len(x),500))
    xLabels = [x[index] for index in xticks]
    # xticks.append(len(x))
    # xLabels.append(lCate[-1][0])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xLabels,rotation=40)

    pyplot.plot(ondurationList)
    pyplot.grid()
    pyplot.show()




fileName = "log.txt"
with open(fileName) as drxFile:
    for line in drxFile:
        # print(line)
        ProcOnduration(line)
        ProcInactivity(line)


draw(xAxis)
# draw2(xAxis)





