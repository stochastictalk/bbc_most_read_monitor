# -*- utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input, Output
import dash_table as dtable
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
df_1 = df.loc[df['RANK']==1, ['TIMESTAMP', 'HEADLINE']] # #1 headlines

# Change column order
df = df[['TIMESTAMP', 'HEADLINE', 'RANK', 'URL']]

# for testing
df_test = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

#pd.DataFrame(
#	{
#	 'Feature A':['Cuthbert', 'Hilbert', 'Dilbert'],
#	 'Feature B':[0.5, 0.1, 0.2]
#	}
#)

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
	  	    		id='date-picker-single-1',
	  	    		date=date.fromtimestamp(df['TIMESTAMP'].max()),
					display_format='Do MMM YYYY'
	  			),
				style={'width':'25%', 'display':'inline-block'}
			),
			dhtml.Div(
				dcc.Slider( # Time slider
			        id='time-slider-1',
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

	dcc.Markdown('', id='headlines-title-output-1'),

	dcc.Markdown('', id='headlines-output-1'),

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
	        id='time-interval-2',
	        options=[
	            {'label': '15 minutes', 'value': '15m'},
	            {'label': '1 hour', 'value': '1h'},
	            {'label': '3 hours', 'value': '3h'},
				{'label': '1 day', 'value':'1d'}
	        ],
	        value='1d'
			),
		style={'width':'30%', 'display':'inline-block'}
		),
		dhtml.Div(
			style={'width':'10%', 'display':'inline-block'}
		),
		dhtml.Div(
			dcc.DatePickerRange(
				id='date-range-2',
		        min_date_allowed=date.fromtimestamp(df['TIMESTAMP'].min()),
		        max_date_allowed=date.fromtimestamp(df['TIMESTAMP'].max()),
		        initial_visible_month=date.fromtimestamp(df['TIMESTAMP'].max()),
				start_date=date.fromtimestamp(df['TIMESTAMP'].max()-7*24*3600),
		        end_date=date.fromtimestamp(df['TIMESTAMP'].max())
			),
		style={'width':'50%', 'display':'inline-block'}
		)
	]),

	dcc.Markdown('', 'confirmation-md-1'),

	dhtml.Br(),

	dhtml.Div(
		dtable.DataTable(
		    id='table-2',
			columns=[{"name": i, "id": i} for i in df_1.columns],
		    data=df_1.to_dict('records'),
    		style_table={'overflowX': 'auto'},
			style_cell_conditional=[
		       {'if': {'column_id': 'TIMESTAMP'},
		        'width': '20%'},
		       {'if': {'column_id': 'HEADLINE'},
				'width': '50%'},
		    ]
		),
		style={'width':'100%'}
	),

	dhtml.Div('hey')

],
style={'width': '60%', 'margin':'auto'}
)

# Define callbacks
# Callback for Viz. 1
@app.callback( # Most Read on DATETIME
	[Output(component_id='headlines-title-output-1',
		 	component_property='children'),
	Output(component_id='headlines-output-1', component_property='children')],
	[Input(component_id='date-picker-single-1', component_property='date'),
	 Input(component_id='time-slider-1', component_property='value')]
)
def update_vis_1(input_yyyy_mm_dd: str, input_hour: float):
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

	f_nearest_ts = datetime.fromtimestamp(nearest_ts).strftime('%A %d %B %Y, %H:%M:%S')
	headlines_title = '** Most Read on {} **'.format(f_nearest_ts)
	return [headlines_title, list_of_headlines]


@app.callback(
	[Output(component_id='table-2', component_property='data')],
	[Input(component_id='date-range-2', component_property='start-date'),
	 Input(component_id='date-range-2', component_property='end-date'),
	 Input(component_id='time-interval-2', component_property='value')]
)
def update_vis_2(start_date, end_date, time_interval):

	return([df_1.loc[:, ['TIMESTAMP', 'HEADLINE']].to_dict('records')])


if __name__ == '__main__':
	app.run_server(debug=True)
