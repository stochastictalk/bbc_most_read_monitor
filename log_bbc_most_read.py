import requests
from datetime import datetime

most_read_url = 'https://www.bbc.co.uk/news/popular/read'
dst_dir = './data/bbc_most_read'
time_of_request = datetime.now().strftime('%s') # time since epoch
timeout = 5 # seconds

# Throws an error if it times out (that's a good thing)
r = requests.get(most_read_url, timeout=timeout)

if 200 <= r.status_code and r.status_code < 300: # request successful
	file = open(dst_dir + '/bbc_most_read_' + time_of_request + '.html', 'w')
	file.write(r.text)
	file.close()
else:
	raise RuntimeError('Request failed: response status code {}.'.format(r.status_code))
