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
	list_of_headlines = [None]*len(file_lines)
	for j, line in enumerate(file_lines):
		list_of_headlines[j] = ','.join(line.split(',')[1:-1]) # headline only
	return(list_of_headlines)

# Gather headlines into a data frame
filepaths = glob('./data/bbc_most_read/*.txt')

# each file contains the 10 most read articles at that timestamp
create_flag = 0
for fp in filepaths:
	unixtime_threshold = 1602011668
	file_unixtime = fp.split('_')[-1][:-4] # omit .txt
	if int(file_unixtime) < unixtime_threshold:
		continue

	# Timestamp, 1, 2, 3, ..., 10
	with open(fp, 'r') as file:
		list_of_headlines = _parse(file.read())
	
	file_df = pd.DataFrame(list_of_headlines, columns=[file_unixtime])
	
	if create_flag == 0:
		headlines_df = file_df
		create_flag = 1
	else:
		headlines_df = headlines_df.join(file_df)
	
print(headlines_df.head(3))
