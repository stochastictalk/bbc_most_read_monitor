# BBC Most Read utilities

# Function that receives HTML of BBC Most Read,
# writes .txt file of headlines of most read articles

import bs4 as bs


def write_headlines_to_disk(html: str, dst_filepath: str):
	'''
	Writes BBC Most Read headlines to a file.
	'''

	file = open(dst_filepath, 'w')

	soup = bs.BeautifulSoup(html, 'html.parser')
	
	for n in range(1, 11):
		r = soup.find(name='li', attrs={'data-entityid':'most-popular-read#{}'.format(n)})
		file.write(_parse_entry(r))

	file.close()


def _parse_entry(entry):
	# Receives li tag with data-entityid=most-popular-read#n
	# Commar-separate headline and number
	split_entry = entry.text.split('\n')
	headline_n = split_entry[2]
	headline_text = split_entry[3]
	headline_url = entry.find('a')['href']
	return(headline_n + ',' + headline_text + ',' + headline_url + '\n')
