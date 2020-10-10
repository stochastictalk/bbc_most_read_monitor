import dash
import dash_core_components as dcc
import dash_html_components as dhtml
import plotly.express as px
import pandas as pd
from glob import glob

def _parse(file_text: str):
	'''
		Receives contents of bbc_most_read_xxxxxxxxxx.txt as string.
		Returns ordered list of headlines, most popular first.
	'''
	file_lines = file_text.split('\n')[:-1]
	dct_of_headlines = {}
	for j, line in enumerate(file_lines):
		dct_of_headlines = ','.join(line.split(',')[1:-1]) # headline only
	return(list_of_headlines)

# Gather headlines into a data frame
filepaths = glob('./data/bbc_most_read/*.txt')

# each file contains the 10 most read articles at that timestamp
for fp in filepaths:
	unixtime_threshold = 1602011668
	file_unixtime = fp.split('_')[-1][:-4] # omit .txt
	if int(file_unixtime) < unixtime_threshold:
		continue

	# Timestamp, 1, 2, 3, ..., 10
	with open(fp, 'r') as file:
		 = _parse(file.read())

	else:
		headlines_df = headlines_df.join(file_df)

print(headlines_df.head(3))
