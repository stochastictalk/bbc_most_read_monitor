# BBC Most Read utilities

import bs4 as bs
import json

def write_headlines_to_disk(html: str, dst_dir: str, timestamp: str):
	'''
	Writes BBC Most Read headlines to a file.

	Args:
		html: string containing html of https://www.bbc.co.uk/news/popular/read
		dst_dr: destination directory filepath
		timestamp: string containing unix time that html was retrieved
	'''

	soup = bs.BeautifulSoup(html, 'html.parser')

	# Gather headlines into a list of dcts, one dct per headline
	list_of_headline_dcts = []
	for n in range(1, 11):
		r = soup.find(name='li', attrs={'data-entityid':'most-popular-read#{}'.format(n)})
		list_of_headline_dcts.append(_parse_entry(r, timestamp))

	# Write list of dcts to .json file
	with open(dst_dir + '/' + timestamp + '.json', 'w') as file:
		file.write(json.dumps(list_of_headline_dcts))


def _parse_entry(entry, timestamp):
	'''
	Receives BeautifulSoup li tag with data-entityid=most-popular-read#n
	Returns dictionary containing a single headline record
'''
	split_entry = entry.text.split('\n')
	headline_n = split_entry[2]
	headline_text = split_entry[3]
	headline_url = entry.find('a')['href']
	headline_dct = {
		'RANK': headline_n,
		'HEADLINE': headline_text,
		'URL': headline_url,
		'TIMESTAMP': timestamp
	}
	return headline_dct
