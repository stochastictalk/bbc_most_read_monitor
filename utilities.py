# -*- utf-8 -*-

import bs4 as bs
import json


def parse_headlines(html: str, timestamp: int):
	''' Parses BBC Most Read HTML for ranked headlines.

	Args:
		html (str): html of Most Read webpage.
		timestamp (int): time that Most Read webpage was retrieved.

	Returns:
		list of dicts: list of dictionaries with keys
					   'rank', 'headline', 'url', 'timestamp'
	'''
	soup = bs.BeautifulSoup(html, 'html.parser')

	# Gather headlines into a list of dcts, one dct per headline
	list_of_headline_dcts = []
	for n in range(1, 11):
		list_tag = soup.find(name='li',
				   	  attrs={'data-entityid':'most-popular-read#{}'.format(n)})
		_, headline_n, headline_text = list_tag.text.split('\n')
		headline_url = list_tag.find('a')['href']
		headline_dct = {
			'RANK': headline_n,
			'HEADLINE': headline_text,
			'URL': headline_url,
			'TIMESTAMP': timestamp
		}
		list_of_headline_dcts += [headline_dct]

	return list_of_headline_dcts



def write_to_disk(html: str, dst_dir: str, timestamp: int):
	'''
	Writes BBC Most Read headlines to a file.

	Args:
		html: string containing html of https://www.bbc.co.uk/news/popular/read
		dst_dr: destination directory filepath
		timestamp: string containing unix time that html was retrieved
	'''

	list_of_headline_dcts = parse_headlines(html, timestamp)

	# Write list of dcts to .json file
	with open(dst_dir + '/' + timestamp + '.json', 'w') as file:
		file.write(json.dumps(list_of_headline_dcts))
