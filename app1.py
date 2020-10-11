import dash
import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input, Output
from datetime import date
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

# Each row is a headline, fields RANK, URL, HEADLINE, TIMESTAMP
df = pd.DataFrame(list_of_records)
df['TIMESTAMP'] = df['TIMESTAMP'].astype(int)
df['RANK'] = df['RANK'].astype(int)

# Want to develop a tool that has a time slider and renders the headlines
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Intialize app obj
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define app layout
app.layout = dhtml.Div([
	dhtml.Div([
	dhtml.H4('BBC Most Read Visualiser V1.0',
			 style={'font-weight':'bold'}),

	dcc.DatePickerSingle(
		calendar_orientation='vertical',
    	id='date-picker-single',
    	date=date.fromtimestamp(df['TIMESTAMP'].max())
	),

	dcc.Slider( # Time slider
        id='time--slider',
        min=0,
        max=24,
        value=18,
        marks={
			t:str(t).zfill(2)+':00' for t in range(0, 25, 2)
		},
        step=0.01,
		included=False
    ),

	dhtml.Br(),

	dcc.Markdown(children='', id='my-output')],
	style={'width': '48%', 'margin':'auto'})
])

# Define callbacks
'''
@app.callback(
	Output(component_id='my-output', component_property='children'),
	[Input(component_id='time--slider', component_property='value')]
)
def update_output_div(input_t):
	#return(input_t)
	# Retrieve headlines for time
	df_rel_entries = df[df['TIMESTAMP']==input_t]
	df_rel_entries.set_index('RANK', inplace=True)

	# Display them
	list_of_headlines = ''.join(
					['{}. {}\n'.format(j,
								df_rel_entries.loc[j,'HEADLINE'])
													for j in range(1, 11)]
											)
	return(list_of_headlines)
'''
if __name__ == '__main__':
	app.run_server(debug=True)
