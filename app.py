import dash
import dash_core_components as dcc
import dash_html_components as dhtml
import plotly.express as px
import pandas as pd
from glob import glob
import json

# Gather headlines into a data frame
filepaths = glob('./data/bbc_most_read/*.json')

# each file contains the 10 most read articles at that timestamp
list_of_records = []
for fp in filepaths:
	with open(fp, 'r') as file:
		file_str = file.read()
	if len(file_str) == 0: # file is empty
		continue
	else:
		list_of_records = list_of_records + json.loads(file_str)

df = pd.DataFrame(list_of_records)

print(df)
