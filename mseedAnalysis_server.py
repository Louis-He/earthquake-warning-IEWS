import matplotlib
matplotlib.use('Agg')

import time

from emailAPI import *
from dataAnalysis import *

latestRecord = []

while True:
    eventList = analysis(net='CI', sta='SLA', loc='00', cha='BHZ')

    newEventStartIdx = newDataReady(latestRecord, eventList)
    if newEventStartIdx != -1:
        for i in range(newEventStartIdx, len(eventList)):
            singleEvent = eventList[i]
            startStr = datetime.datetime.utcfromtimestamp(singleEvent["timeStart"]).strftime('%Y-%m-%d %H:%M:%S.%f')[
                       :-3]
            endStr = datetime.datetime.utcfromtimestamp(singleEvent["timeEnd"]).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            mag = round(transferToMagnitude(singleEvent["peakVel"] * math.sqrt(3)), 2)
            print(startStr, endStr, round(transferToMagnitude(singleEvent["peakVel"] * math.sqrt(3)), 2))

            emailNotification(mag, startStr)

    latestRecord = eventList
    time.sleep(1)