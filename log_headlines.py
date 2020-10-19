# -*- utf-8 -*-
import requests
from datetime import datetime
import utilities as util

most_read_url = 'https://www.bbc.co.uk/news/popular/read'
dst_dir = '/home/jerome/Documents/bbc_most_read_monitor/data/bbc_most_read'
time_of_request = int(datetime.now().strftime('%s')) # time since epoch
timeout = 15 # seconds

# Throws an error if it times out (that's a good thing)
headers = {'User-Agent':'Mozilla/5.0'}
r = requests.get(most_read_url, timeout=timeout, headers=headers)

if 200 <= r.status_code and r.status_code < 300: # request successful
	list_of_headline_dcts = util.parse_headlines(r.text, time_of_request)
	util.write_to_disk(list_of_headline_dcts, dst_dir, time_of_request)
	util.write_to_sql(list_of_headline_dcts)
else:
	raise RuntimeError('Request failed: response status code {}.'.format(r.status_code))
