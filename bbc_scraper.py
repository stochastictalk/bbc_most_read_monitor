# Script for scraping the BBC headlines

import bs4 as bs
import requests

headline_src_url = 'https://bbc.co.uk/news'
r = requests.get(headline_src_url)
soup = bs.BeautifulSoup(r.text, 'html.parser')
