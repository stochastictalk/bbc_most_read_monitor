import requests
import bs4 as bs
from os import mkdir

homepage_urls = {
	'Guardian':'https://www.theguardian.com/uk',
	'Times':'https://www.thetimes.co.uk/',
	'BBC':'https://www.bbc.co.uk/news',
	'Daily Mail':'https://www.dailymail.co.uk/home/index.html',
	'Sun':'https://www.thesun.co.uk/',
	'Independent':'https://www.independent.co.uk/',
	'Financial Times':'https://www.ft.com/',
}
