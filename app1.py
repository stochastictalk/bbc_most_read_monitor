# -*- utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input, Output
from datetime import datetime, date, timezone, timedelta
import plotly.express as px
import pandas as pd
from glob import glob
import json
import numpy as np

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
	dhtml.H4('BBC Most Read Visualiser V1.0',
			 style={'font-weight':'bold'}),
	dhtml.P('''
			This app allows you to explore the most read articles on BBC News \
			over time.

	  		'''),

	dhtml.Hr(),

	# 1. Most Read on DATETIME
	dhtml.H5('The 10 Most Read articles over time',
			 style={'font-weight':'bold'}),

	dhtml.Div([
			dhtml.Div('Date',
					  style={'font-weight':'bold',
							 'width':'25%',
							 'display':'inline-block'}),
			dhtml.Div('Time of day (UTC)',
					  style={'font-weight':'bold',
							 'width':'75%',
							 'display':'inline-block'})
			],
		style={'width':'100%', 'display':'inline-block'}
	),

	dhtml.Div([
			dhtml.Div(
	  			dcc.DatePickerSingle(
	  	    		id='1-date-picker-single',
	  	    		date=date.fromtimestamp(df['TIMESTAMP'].max()),
					display_format='Do MMM YYYY'
	  			),
				style={'width':'25%', 'display':'inline-block'}
			),
			dhtml.Div(
				dcc.Slider( # Time slider
			        id='1-time-slider',
			        min=0,
			        max=24,
			        value=18,
			        marks={
						t:str(t).zfill(2)+':00' for t in range(0, 25, 2)
					},
			        step=0.25,
					included=False,
				),
				style={'width':'75%', 'display':'inline-block'}
			)]),

	dhtml.Br(),

	dcc.Markdown(children='', id='headlines-title-output'),

	dcc.Markdown(children='', id='headlines-output'),

	dhtml.Div(
		dhtml.Hr(),
		style={'width':'100%'}
	),

	# 2. MOST READ TIMELINE - choose time interval, date range
	dhtml.H5('#1 Most Read article over time',
			 style={'font-weight':'bold'}),

	dhtml.Div([
		dhtml.Div(
			'Time interval',
			style={'font-weight':'bold',
			       'width':'30%',
				   'display':'inline-block'}
		),
		dhtml.Div(
			style={'width':'10%', 'display':'inline-block'}
		),
		dhtml.Div(
			'Date range',
			style={'font-weight':'bold',
			       'width':'50%',
				   'display':'inline-block'}
		)
	],
	style={'width':'100%'}
	),

	dhtml.Div([
		dhtml.Div(
			dcc.Dropdown(
	        id='2-time-interval',
	        options=[
	            {'label': '15 minutes', 'value': '15m'},
	            {'label': '1 hour', 'value': '1hr'},
	            {'label': '3 hours', 'value': '3hr'},
				{'label': '1 day', 'value':'1d'}
	        ],
	        value='NYC'
			),
		style={'width':'30%', 'display':'inline-block'}
		),
		dhtml.Div(
			style={'width':'10%', 'display':'inline-block'}
		),
		dhtml.Div(
			dcc.DatePickerRange(
				id='2-date-range',
		        min_date_allowed=date.fromtimestamp(df['TIMESTAMP'].min()),
		        max_date_allowed=date.fromtimestamp(df['TIMESTAMP'].max()),
		        initial_visible_month=date.fromtimestamp(df['TIMESTAMP'].max()),
		        end_date=date.fromtimestamp(df['TIMESTAMP'].max())
			),
		style={'width':'50%', 'display':'inline-block'}
		)
	]),
],
style={'width': '48%', 'margin':'auto'})

# Define callbacks
@app.callback( # Most Read on DATETIME
	[Output(component_id='headlines-title-output',
		 	component_property='children'),
	Output(component_id='headlines-output', component_property='children')],
	[Input(component_id='1-date-picker-single', component_property='date'),
	 Input(component_id='1-time-slider', component_property='value')]
)
def update_output_div(input_yyyy_mm_dd: str, input_hour: float):
	# Get the time, convert it to the nearest fifteen-minute timestamp
	date_ts = datetime.strptime(input_yyyy_mm_dd, "%Y-%m-%d").timestamp()
	ts = date_ts + input_hour*3600

	unique_ts = df['TIMESTAMP'].unique() # numpy array
	nearest_ts = unique_ts[np.argmin(np.abs(unique_ts - ts))]

	# Retrieve headlines for time
	df_rel_entries = df[df['TIMESTAMP']==nearest_ts]
	df_rel_entries.set_index('RANK', inplace=True)

	# Display them
	bbc_root_dir = 'https://bbc.com'
	list_of_headlines = ''.join(
					['{}. [{}]({})\n'.format(j,
								df_rel_entries.loc[j,'HEADLINE'],
								bbc_root_dir+df_rel_entries.loc[j, 'URL'])
													for j in range(1, 11)]
											)

	f_nearest_ts = datetime.fromtimestamp(nearest_ts).strftime(
														'%A %d %B %Y, %H:%M:%S')
	headlines_title = '** Most Read on {} **'.format(f_nearest_ts)
	return [headlines_title, list_of_headlines]

if __name__ == '__main__':
	app.run_server(debug=True)
