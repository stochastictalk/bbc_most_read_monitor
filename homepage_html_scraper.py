import requests
import bs4 as bs
from os import mkdir
from os.path import exists
from datetime import datetime

date_str = datetime.now().strftime('%a_%d_%m_%y')

headers = { # necessary for scraping The Sun
	'User-Agent':'Mozilla/5.0'
}

homepage_urls = {
	'Guardian':'https://www.theguardian.com/uk',
	'Times':'https://www.thetimes.co.uk/',
	'BBC':'https://www.bbc.co.uk/news',
	'Daily Mail':'https://www.dailymail.co.uk/home/index.html',
	'Sun':'https://www.thesun.co.uk/',
	'Independent':'https://www.independent.co.uk/',
	'Financial Times':'https://www.ft.com/',
}


for name, url in homepage_urls.items():
	if not exists('./data/' + name + '/'):
		mkdir('./data/' + name + '/')

	dst_path = './data/' + name + '/' + date_str + '.html'

	try:
		r = requests.get(url, headers=headers, timeout=5)
	except requests.exceptions.ReadTimeout:
		continue	

	dst_file = open(dst_path, 'w')
	dst_file.write(r.text)
	dst_file.close()
