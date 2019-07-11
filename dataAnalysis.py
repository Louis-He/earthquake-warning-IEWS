from obspy.core import UTCDateTime
from obspy import read

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

import math
import datetime

def transferToMagnitude(velocity):
    mag = 0

    if(velocity <= 0.1):
        mag =  velocity / 0.1 * 1.7
    elif(velocity <= 1.1):
        mag = (velocity - 0.1) / (1.1 - 0.1) * (3 - 1.7) + 1.7
    elif (velocity <= 3.4):
        mag = (velocity - 1.1) / (3.4 - 1.1) * (3.6 - 3) + 3
    elif (velocity <= 8.1):
        mag = (velocity - 3.4) / (8.1 - 3.4) * (4.1 - 3.6) + 3.6
    elif (velocity <= 16):
        mag = (velocity - 8.1) / (16 - 8.1) * (4.7 - 4.1) + 4.1
    elif (velocity <= 31):
        mag = (velocity - 16) / (31 - 16) * (5.25 - 4.7) + 4.7
    elif (velocity <= 60):
        mag = (velocity - 31) / (60 - 31) * (5.9 - 5.25) + 5.25
    elif (velocity <= 116):
        mag = (velocity - 60) / (116 - 60) * (6.7 - 5.9) + 5.9
    elif (velocity > 116):
        mag = 9999

    return mag

def transferToIntensity(velocity):
    Intensity = 0
    if(velocity < 0.1):
        Intensity = 1
    elif(velocity <= 0.4):
        Intensity = 2
    elif(velocity <= 1.1):
        Intensity = 3
    elif (velocity <= 3.4):
        Intensity = 4
    elif (velocity <= 8.1):
        Intensity = 5
    elif (velocity <= 16):
        Intensity = 6
    elif (velocity <= 31):
        Intensity = 7
    elif (velocity <= 60):
        Intensity = 8
    elif (velocity <= 116):
        Intensity = 9
    else:
        Intensity = 10

    return Intensity

def magnitudeToText(mag):
    if(mag != 9999):
        return str(mag)
    else:
        return "> 6.7"

def processSingleChannelData(velocityArr):
    maximum = max(velocityArr)
    maximum *= math.sqrt(3)
    maxMagnitude = transferToMagnitude(maximum)

    return maxMagnitude

# tolerence in sample length for one side
def clusterSingleEvent(boolSeq, tolerence):
    originalSeq = boolSeq.copy()

    # clutser single event
    for i in range(len(boolSeq)):
        if(boolSeq[i] == False):
            if(i > 0 and originalSeq[i - 1] == True):
                boolSeq[i] = True
            else:
                for j in range(-tolerence + 1, tolerence):
                    if(i + j >= 0 and i + j < len(boolSeq) and originalSeq[i + j] == True):
                        boolSeq[i] = True

    return boolSeq

# shortestPeriod in sample length
def extractEarthquakeSeries(boolSeq, shortestPeriod):
    timeIdxSeries = []
    isEarthquake = False
    count = 0

    for i in boolSeq:
        if isEarthquake == False and i == True:
            isEarthquake = True
            timeIdxSeries.append([count, -1])
        if isEarthquake == True and i == False:
            isEarthquake = False
            startIdx = timeIdxSeries[len(timeIdxSeries) - 1][0]
            if(count - startIdx < shortestPeriod):
                del timeIdxSeries[len(timeIdxSeries) - 1]
            else:
                timeIdxSeries[len(timeIdxSeries) - 1][1] = count
        count += 1

    return timeIdxSeries

# tolerence in m/s
def identifyEvent(trace, tolerence):
    earthquakeList = []

    traceArr = trace.data
    traceLength = len(traceArr)
    earthquakeBool = [False] * traceLength

    for i in range(traceLength):
        if(abs(traceArr[i]) > tolerence):
            earthquakeBool[i] = True

    earthquakeBool = clusterSingleEvent(earthquakeBool, 40)
    earthquakeTimeIdxSeries = extractEarthquakeSeries(earthquakeBool, shortestPeriod = 10)

    matplotlibTimes = trace.times("timestamp")
    for singleEventTimeIdx in earthquakeTimeIdxSeries:
        maxMag = 0.0
        startIdx = singleEventTimeIdx[0]
        endIdx = singleEventTimeIdx[1]
        if endIdx == -1:
            endIdx = traceLength - 1

        timeStart = matplotlibTimes[startIdx]
        timeEnd = matplotlibTimes[endIdx]

        for i in range(startIdx, endIdx):
            if(abs(traceArr[i]) > maxMag):
                maxMag = abs(traceArr[i])

        earthquakeList.append({
            "timeStart": timeStart,
            "timeEnd": timeEnd,
            "length": timeEnd - timeStart,
            "peakVel": maxMag,
        })

    return earthquakeList

def draw(traceFile, maxMag, magNow):
    # graph start
    fig, axs = plt.subplots(1, 1)
    fig.set_size_inches(11, 5)

    axs.clear()

    at = AnchoredText(traceFile[0].id, loc='upper left', prop=dict(size=8), frameon=True)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    axs.add_artist(at)

    axs.plot(traceFile[0].times("matplotlib"), traceFile[0].data, '#000000')
    axs.xaxis_date()
    axs.set_xlabel('time')
    axs.set_ylabel('velocity(m/s)')
    fig.autofmt_xdate()

    axs.set_xlim([datetime.datetime.utcnow() - datetime.timedelta(minutes=10), datetime.datetime.utcnow()])
    plt.title("Realtime Seismic Wave(SLA) - Past 10 minutes")
    # graph end

    if(len(traceFile[0].data) > 40 * 60 * 10):
        traceFile[0].data = traceFile[0].data[-40 * 60 * 10:]

    at = AnchoredText("MaxMag   MagNow\n   " + maxMag + "         " + magNow, loc='upper right',
                      prop=dict(size=16, color='#FF0000'), frameon=True)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    axs.add_artist(at)
    plt.savefig('latest_' + traceFile[0].id + '.png')
    plt.close(fig)

# return the initial Idx where is a new seismic event
def newDataReady(latestRecord, newList):
    if(len(newList) == 0):
        return -1

    if(len(latestRecord) == 0):
        return 0
    else:
        currentSeismicEventIdx = len(newList) - 1
        lastRecord = latestRecord[len(latestRecord) - 1]

        while(not (abs(newList[currentSeismicEventIdx]["timeStart"] - lastRecord["timeStart"])) < 0.1):
            currentSeismicEventIdx -= 1
            if(currentSeismicEventIdx == -1):
                return 0

        if((abs(newList[currentSeismicEventIdx]["peakVel"] - lastRecord["peakVel"])) < 0.01):
            if(currentSeismicEventIdx == len(newList) - 1):
                return -1
            else:
                return currentSeismicEventIdx + 1
        else:
            return currentSeismicEventIdx

def analysis(net, sta, loc, cha):
    day = UTCDateTime.now().strftime('%Y.%j')
    fn = 'data/%s.%s.%s.%s.D.%s' % (net, sta, loc, cha, day)
    try:
        traceFile = read(fn)
        traceFile.filter("highpass", freq = 1.0)
    except:
        print('ERROR reading File')
        return []

    for i in range(len(traceFile[0])):
        (traceFile[0].data)[i] /= 6.27368E8
        (traceFile[0].data)[i] *= 100

    t = traceFile[0].stats.endtime
    traceFile.trim(t - 10 * 60, t)
    traceCopy = traceFile[0].copy()

    maxMag = magnitudeToText(round(processSingleChannelData(traceFile[0].data), 2))
    magNow = magnitudeToText(round(processSingleChannelData(traceFile[0].data[-40 * 30:]), 2))

    draw(traceFile, maxMag, magNow)

    eventList = identifyEvent(trace=traceCopy, tolerence=0.00028)

    return eventList