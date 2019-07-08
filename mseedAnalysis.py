from obspy.core.trace import Trace
from obspy.core import UTCDateTime
from obspy import read

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import matplotlib.animation as animation
import datetime
import math

#
#

net = 'CI' # network code
sta = 'SLA' # station name
cha = 'BHZ' # channel

loc = '00'

# begin the graph
fig, axs = plt.subplots(1, 1)
fig.set_size_inches(8, 5)

def transferToIntensity(velocity):
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

def magnitudeToText(mag):
    if(mag != 9999):
        return str(mag)
    else:
        return "> 6.7"

def processArrData(velocityArr):
    maximum = max(velocityArr)
    maxMagnitude = transferToIntensity(maximum)

    return maxMagnitude


def animate(i):
    day = UTCDateTime.now().strftime('%Y.%j')
    fn = 'data/%s.%s.%s.%s.D.%s' % (net, sta, loc, cha, day)
    traceFile = read(fn)
    traceFile.filter("highpass", freq = 1.0)

    for i in range(len(traceFile[0])):
        (traceFile[0].data)[i] /= 6.27368E8
        (traceFile[0].data)[i] *= 100
    # Trace.plot(traceFile)

    # graph start
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

    at = AnchoredText("MaxMag   MagNow\n   " + magnitudeToText(round(processArrData(traceFile[0].data) * math.sqrt(3), 2)) +
                      "         " + magnitudeToText(round(processArrData(traceFile[0].data[-40 * 30:]) * math.sqrt(3), 2)), loc='upper right',
                      prop=dict(size=16, color='#FF0000'), frameon=True)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    axs.add_artist(at)

ani = animation.FuncAnimation(fig, animate, interval=2000)
plt.show()
'''
#
#
traceFile = read('data/CI.ISA.00.BHZ.D.2019.189')
traceFile.filter("highpass", freq = 1.0)

for i in range(len(traceFile[0])):
    (traceFile[0].data)[i] /= 5.4413599E9
    (traceFile[0].data)[i] *= 100
Trace.plot(traceFile)

#
#
traceFile = read('data/CI.PASC.00.BHZ.D.2019.189')
traceFile.filter("highpass", freq = 1.0)

for i in range(len(traceFile[0])):
    (traceFile[0].data)[i] /= 5.9389701E9
    (traceFile[0].data)[i] *= 100
Trace.plot(traceFile)
'''