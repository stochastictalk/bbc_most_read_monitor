# -*- utf-8 -*-
import bs4 as bs
import json
import psycopg2

import db_creds

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
		_, _, headline_n, headline_text, _, _ = list_tag.text.split('\n')
		print(headline_n)
		headline_url = list_tag.find('a')['href']
		headline_dct = {
			'rank': headline_n,
			'headline': headline_text,
			'url': headline_url,
			'timestamp': timestamp
		}
		list_of_headline_dcts += [headline_dct]

	return list_of_headline_dcts



def write_to_disk(list_of_headline_dcts: list, dst_dir: str, timestamp: int):
	'''
	Writes BBC Most Read headlines to a file.

	Args:
		list_of_headline_dcts: as returned by parse_headlines().
		html: string containing html of https://www.bbc.co.uk/news/popular/read
		dst_dr: destination directory filepath
	'''

	# Write list of dcts to .json file
	with open(dst_dir + '/' + str(timestamp) + '.json', 'w') as file:
		file.write(json.dumps(list_of_headline_dcts))

def write_to_sql(list_of_headlines_dct, relation_name='headlines'):
	''' Writes a list of headline dicts to SQL relation 'relation_name'
		in db 'bbc_most_read'

		a headline_dct: {'rank':int, 'headline':str, 'url':str, 'timestamp':int}
	'''
	conn = 	psycopg2.connect(user=db_creds.user,
							 password=db_creds.password,
						 	 host=db_creds.host,
							 port=db_creds.port,
							 database=db_creds.database)
	cursor = conn.cursor()
	for l in list_of_headlines_dct:
		sql_command = ('INSERT INTO ' + relation_name +
					   ' (rank_, headline, url, timestamp_)' +
					   ' VALUES ({}, \'{}\', \'{}\', {})'.format(
					   						l['rank'],
					   						l['headline'].replace('\'', '\'\''),
											l['url'].replace('\'', '\'\''),
											l['timestamp']))
		cursor.execute(sql_command)

	conn.commit()
	cursor.close()
	conn.close()
