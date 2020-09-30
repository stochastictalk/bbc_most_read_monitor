# Script for scraping the BBC headlines

import bs4 as bs
import requests

headline_src_url = 'https://bbc.co.uk/news')
r = requests.get(headline_src_url)
html = r.text
soup = bs.BeautifulSoup(html, 'html.parser')
