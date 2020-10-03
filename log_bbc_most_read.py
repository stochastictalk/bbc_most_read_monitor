import requests
from datetime import datetime
from bbc_most_read_utilities import write_headlines_to_disk

most_read_url = 'https://www.bbc.co.uk/news/popular/read'
dst_dir = '/home/jerome/Documents/headline_monitor/data/bbc_most_read'
time_of_request = datetime.now().strftime('%s') # time since epoch
timeout = 15 # seconds

# Throws an error if it times out (that's a good thing)
r = requests.get(most_read_url, timeout=timeout)

if 200 <= r.status_code and r.status_code < 300: # request successful
	#file = open(dst_dir + '/bbc_most_read_' + time_of_request + '.html', 'w')
	#file.write(r.text)
	#file.close()
	dst_filepath = dst_dir + '/bbc_most_read_' + time_of_request + '.txt'
	write_headlines_to_disk(r.text, dst_filepath)
else:
	raise RuntimeError('Request failed: response status code {}.'.format(r.status_code))
