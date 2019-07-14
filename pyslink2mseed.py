from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient
from obspy.core.stream import read
from obspy.core import UTCDateTime

import os
import requests
import threading

from setting import *

class sockectThread (threading.Thread):
	def __init__(self, threadID, stationInfoDict):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.stationInfo = stationInfoDict

	def run(self):
		# client_addr is in address:port format
		net = self.stationInfo["net"]  # network code
		sta = self.stationInfo["sta"]  # station name
		cha = self.stationInfo["cha"]  # channel

		loc = self.stationInfo["loc"]  # Since obspy doesn't take location codes, this only affects the filename
		multipleLoc = self.stationInfo["multipleLoc"]

		# Connect to a SeedLink server
		client = MyClient(net, sta, cha, loc, multipleLoc, client_addr)

		# Retrieve INFO:STREAMS
		# streams_xml = client.get_info('STREAMS')
		# print(streams_xml)

		print("Start Connecting to %s-%s-%s" % (net, sta, cha))
		# Select a stream and start receiving data
		client.select_stream(net, sta, cha)
		client.run()
		print("End threading：" + self.threadID)

# Subclass the client class
class MyClient(EasySeedLinkClient):
	def __init__(self, net, sta, cha, loc, multipleLoc, *args, **kwargs):
		self.net = net
		self.sta = sta
		self.cha = cha
		self.loc = loc
		self.multipleLoc = multipleLoc
		super().__init__(*args, **kwargs)

	# Implement the on_data callback
	def on_data(self, trace):
		# in case multiple loc in one station
		if (self.multipleLoc and trace.get_id().find(self.loc) == -1):
			return

		day = UTCDateTime.now().strftime('%Y.%j')
		fn = 'data/%s.%s.%s.%s.D.%s' % (self.net, self.sta, self.loc, self.cha, day)

		print('Received traces. Checking for existing data...')
		if (os.path.isfile(fn)):
			print('Found %s, reading...' % fn)
			originalTraces = read(fn)
			traces = originalTraces + trace
		else:
			print('No data found. Creating new blank trace to write to...')
			traces = trace
		print('Trace: %s' %(trace))

		print('Saving traces to %s...' % (fn))
		traces.write(fn, format='MSEED')
		print('Done.')
		if(updateStatus):
			try:
				requests.request(url='http://0.0.0.0:8088/updateSocket', method='GET')
			except:
				print('Cannot update status.')

# Create multithreading according to setting
if(len(stations) > 5):
	print("[Error] More than 5 stations are selected.")
	exit(0)

threadingList = []
threadIdx = 0
for station in stations:
	threadingList.append(sockectThread(threadIdx, station))
	threadIdx += 1

threadIdx = 0
for thread in threadingList:
	thread.start()
	print(str(threadIdx) + 'start.')
	threadIdx += 1