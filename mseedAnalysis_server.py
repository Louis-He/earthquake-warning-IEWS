import matplotlib
matplotlib.use('Agg')

import time
import requests

from emailAPI import *
from dataAnalysis import *

latestRecord = []

# emailNotification(9.0, "***** TEST ***** TEST ***** TEST *****")
while True:
    eventList = analysis(net='CI', sta='SLA', loc='00', cha='BHZ')

    newEventStartIdx = newDataReady(latestRecord, eventList)
    if newEventStartIdx != -1:
        for i in range(newEventStartIdx, len(eventList)):
            singleEvent = eventList[i]
            startStr = datetime.datetime.utcfromtimestamp(singleEvent["timeStart"]).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            endStr = datetime.datetime.utcfromtimestamp(singleEvent["timeEnd"]).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            mag = round(transferToMagnitude(singleEvent["peakVel"] * math.sqrt(3)), 2)
            print(startStr, endStr, mag)

            emailNotification(mag, startStr)

    latestRecord = eventList
    try:
        requests.request(url='http://0.0.0.0:8088/updateAnalysis', method='GET')
    except:
        print('Cannot update status.')

    time.sleep(1)