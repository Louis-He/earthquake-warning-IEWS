from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient
from obspy.core.trace import Trace
from obspy.core.stream import read
from obspy.core import UTCDateTime
import os

# client_addr is in address:port format
client_addr = 'rtserve.iris.washington.edu:18000'
net = 'CI' # network code
sta = 'SLA' # station name
cha = 'BHZ' # channel

loc = '00' # Since obspy doesn't take location codes, this only affects the filename

# Subclass the client class
class MyClient(EasySeedLinkClient):
	# Implement the on_data callback
	def on_data(self, trace):
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

# Connect to a SeedLink server
client = MyClient(client_addr)

# Retrieve INFO:STREAMS
streams_xml = client.get_info('STREAMS')
print(streams_xml)

# Select a stream and start receiving data
client.select_stream(net, sta, cha)
client.run()
