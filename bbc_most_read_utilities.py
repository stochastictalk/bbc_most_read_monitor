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
		file.write(r.text)

	file.close()

