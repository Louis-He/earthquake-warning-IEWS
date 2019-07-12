from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient
from obspy.core.stream import read
from obspy.core import UTCDateTime

import os
import requests

from setting import *

# client_addr is in address:port format
net = 'CI' # network code
sta = 'SLA' # station name
cha = 'BHZ' # channel

loc = '00' # Since obspy doesn't take location codes, this only affects the filename
multipleLoc = False

# Subclass the client class
class MyClient(EasySeedLinkClient):
	# Implement the on_data callback
	def on_data(self, trace):

		# in case multiple loc in one station
		if (multipleLoc and trace.get_id().find(loc) == -1):
			return

		day = UTCDateTime.now().strftime('%Y.%j')
		fn = 'data/%s.%s.%s.%s.D.%s' % (net, sta, loc, cha, day)

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
		try:
			requests.request(url='http://0.0.0.0:8088/updateSocket', method='GET')
		except:
			print('Cannot update status.')

# Connect to a SeedLink server
client = MyClient(client_addr)

# Retrieve INFO:STREAMS
streams_xml = client.get_info('STREAMS')
print(streams_xml)

# Select a stream and start receiving data
client.select_stream(net, sta, cha)
client.run()

print('A')