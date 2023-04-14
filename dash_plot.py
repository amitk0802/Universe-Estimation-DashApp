# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:29:21 2020

@author: kaam8004
"""

import base64
import datetime
import io
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
import calendar
import numpy as np
import os
from plotly import graph_objs as go
import plotly.express as px


# Temporay directory
tem_dir = r"C:\Users\amkasera2001\Desktop\Python/"

#external_scripts = ['src': '']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, )

input_data = pd.DataFrame()

# ######################## LAYOUT STARTING ###################################

app.layout = html.Div([
    dcc.Tabs([

# Input Tab
        dcc.Tab(label='Input', children=[
            html.Hr(),
            html.H1(children='DAR Application',
                    style={
                        'textAlign': 'center',
                        'color': '#7FDBFF'
                    }
                    ),    
            html.Hr(),
            html.Div([
                html.Label("Enter the Start Date : "),
                dcc.Input(id="input1", type="text", placeholder="YYYY-MM-DD")
                ]             
                ),

            html.Br(),

            html.Div([            
                html.Label("Enter the End Date((3000-12-31)) : "),
                dcc.Input(id="input2", type="text", placeholder="YYYY-MM-DD")
                ]
                ),

            html.Br(),
            
            html.Label("Select Country : "),
            dcc.Dropdown(
                id='country-id',
                options=[
                    {'label': 'Belgium', 'value': 'BE'},
                    {'label': 'Bulgaria', 'value': 'BG'},
                    {'label': 'Canada', 'value': 'CA'},
                    {'label': 'Czechia', 'value': 'CZ'},
                    {'label': 'Denmark', 'value': 'DK'},
                    {'label': 'France', 'value': 'FR'},
                    {'label': 'Germany', 'value': 'DE'},
                    {'label': 'Greece', 'value': 'GR'},
                    {'label': 'Hungary', 'value': 'HU'},
                    {'label': 'Ireland', 'value': 'IE'},
                    {'label': 'Israel', 'value': 'IL'},
                    {'label': 'Italy', 'value': 'IT'},
                    {'label': 'Netherland', 'value': 'NL'},
                    {'label': 'Norway', 'value': 'NO'},
                    {'label': 'Poland', 'value': 'PL'},
                    {'label': 'Spain', 'value': 'ES'},
                    {'label': 'Sweden', 'value': 'SE'},
                    {'label': 'Turkey', 'value': 'TR'},
                    {'label': 'UAE', 'value': 'AE'},            
                    {'label': 'Unikted Kingdom', 'value': 'GB'},

                ],
                placeholder="Select a Country",
                style={'height': '30px', 'width': '250px'}    ),

                html.Br(),

        dcc.Upload(
                id='input-data',
                children=html.Div([
                    'INPUT FILE- Drag and Drop or ',
                    html.A('Select File')
                ]),
                style={
                    'width': '50%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='input-data-upload'),

                html.Br(),

        dcc.Upload(
                id='previous-data',
                children=html.Div([
                    'PREVIOUS FILE- Drag and Drop or ',
                    html.A('Select File')
                ]),
                style={
                    'width': '50%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='previous-data-upload'),

                html.Br(),

            html.Button('Submit', id='submit-val',n_clicks=0),
            ],),

# Output Tab
        dcc.Tab(label='Output', children=[
            html.Div(id='output-file')
            ])
        ])
    
])

# ############################### LAYOUT ENDS ################################


# Function to show file in table form

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),

        dash_table.DataTable(
            style_table={
                'width': '50%',
            },
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={'padding': '10px',
                        'maxWidth': 0,
                        'height': 20,
                        'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'color': 'black'
            },
            style_cell_conditional=[],
            virtualization=True,
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


# Save files in local system
def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(tem_dir, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


@app.callback(Output('input-data-upload', 'children'),
              [Input('input-data', 'contents')],
              [State('input-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        for   c, n in zip(list_of_contents, list_of_names):
            save_file('File1.xlsx', c)
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


@app.callback(Output('previous-data-upload', 'children'),
              [Input('previous-data', 'contents')],
              [State('previous-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        for   c, n in zip(list_of_contents, list_of_names):
            save_file('File2.csv', c)
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


@app.callback(Output('output-file', 'children'),
              [Input('submit-val', 'n_clicks'),], [ State('input1', 'value'), State('input2', 'value'), State('country-id', 'value')])
def update_output(clicks, start_date, end_date, countryid):
    if clicks>0:
        children = output_contents(start_date, end_date, countryid)
        return children
    else:
        pass

def output_test(start_date, end_date, countryid):
    path = r'C:\Digital_UE\DAR UE\DAR\2020'
    country_id = countryid                    # App
    today = str(datetime.date.today())
    year = int(today[:4])
    month = int(today[5:7])
    UE_start_date = start_date                # App
    UE_end_date = end_date                    # App
    return html.Div([
        'Variables are {} {} {} {} {} {} {}'.format(year, month, path, country_id, today, UE_start_date, UE_end_date),
        ])

def output_contents(start_date, end_date, countryid):
    
# Declaring Variables
    base_path = r'C:\Digital_UE\DAR UE\DAR'
    country_id = countryid                 # App
    today = str(datetime.date.today())
    year = int(today[:4])
    path = base_path + '\\' + str(year) + '\\' + country_id
    mon = int(today[5:7])
    # Creating output folder
    if not os.path.exists(path):
        os.makedirs(path)
    
    month = (calendar.month_name[mon][:3]).lower()
    UE_start_date = start_date                  # App
    UE_end_date = end_date                    # App
    input_file = pd.read_excel(r'C:\Users\amkasera2001\Desktop\Python\File1.xlsx'
                 , index_col = 0, dtype = {'Male X 1000': float, 'Female X 1000': float}
                 , skiprows = 1)
    csv_output_file = path + '\\universe_estimate_' + country_id.lower() + '_' + str(month) + '_' + str(year) +'.csv'
    txt_output_file = path + '\\universe_estimate_' + country_id.lower() + '_' + str(month) + '_' + str(year) +'.txt'
    prev_yr_csv_file = r'C:\Users\amkasera2001\Desktop\Python\File2.csv'
    compare_file = path + '\\DAR_Compare_' + country_id +'_UEs_'+ str(year) +'.csv'

# Listing age groups meant for intermediate table
    age_groups = ['2-11',
                  '12-12',
                  '13-14', 
                  '15-17',
                  '18-20',
                  '21-24',
                  '25-29',
                  '30-34',
                  '35-39',
                  '40-44',
                  '45-49',
                  '50-54',
                  '55-64',
                  '65+'
    ]

# Preparing dictionary containing demo_id for final table with corresponding age bucket
    demo_id =  { 2: ['2-11'],
                13: ['13-14'],
                14: ['12-12'],
                15: ['15-17'],
                18: ['18-20'],
                21: ['21-24'],
                25: ['25-29'],
                30: ['30-34'],
                35: ['35-39'],
                40: ['40-44'],
                45: ['45-49'],
                50: ['50-54'],
                55: ['55-64'], 
                65: ['65+']}

# Preparing two intermediate tables (one for male and another for female)
    male = intermed(input_file,'M',input_file['Male'], age_groups)
    female = intermed(input_file, 'F', input_file['Female'], age_groups)
    
# Combining both male and female
    intermediate = pd.concat([female, male])
        
# Preparing two final tables (one for male and another for female)
    out_fem = final(female, demo_id)
    out_mal = final(male, demo_id)
    
    out_fem.loc[out_fem['demo_id'] == 2, 'demo_id'] = 'F:02-12'
    out_fem.loc[out_fem['demo_id'] == 14, 'demo_id'] = 'F:02-12'
    out_fem.loc[out_fem['demo_id'] == 13, 'demo_id'] = 'F:13-17'
    out_fem.loc[out_fem['demo_id'] == 15, 'demo_id'] = 'F:13-17'
    out_fem.loc[out_fem['demo_id'] == 18, 'demo_id'] = 'F:18-20'
    out_fem.loc[out_fem['demo_id'] == 21, 'demo_id'] = 'F:21-24'
    out_fem.loc[out_fem['demo_id'] == 25, 'demo_id'] = 'F:25-29'
    out_fem.loc[out_fem['demo_id'] == 30, 'demo_id'] = 'F:30-34'
    out_fem.loc[out_fem['demo_id'] == 35, 'demo_id'] = 'F:35-39'
    out_fem.loc[out_fem['demo_id'] == 40, 'demo_id'] = 'F:40-44'
    out_fem.loc[out_fem['demo_id'] == 45, 'demo_id'] = 'F:45-49'
    out_fem.loc[out_fem['demo_id'] == 50, 'demo_id'] = 'F:50-54'
    out_fem.loc[out_fem['demo_id'] == 55, 'demo_id'] = 'F:55-64'
    out_fem.loc[out_fem['demo_id'] == 65, 'demo_id'] = 'F:65+'
    out_fem = out_fem.groupby(['demo_id'])['UE'].sum()
    out_fem = out_fem.to_frame()
    out_fem.reset_index(inplace=True)
    
    out_mal.loc[out_mal['demo_id'] == 2, 'demo_id'] = 'F:02-12'
    out_mal.loc[out_mal['demo_id'] == 14, 'demo_id'] = 'F:02-12'
    out_mal.loc[out_mal['demo_id'] == 13, 'demo_id'] = 'F:13-17'
    out_mal.loc[out_mal['demo_id'] == 15, 'demo_id'] = 'F:13-17'
    out_mal.loc[out_mal['demo_id'] == 18, 'demo_id'] = 'F:18-20'
    out_mal.loc[out_mal['demo_id'] == 21, 'demo_id'] = 'F:21-24'
    out_mal.loc[out_mal['demo_id'] == 25, 'demo_id'] = 'F:25-29'
    out_mal.loc[out_mal['demo_id'] == 30, 'demo_id'] = 'F:30-34'
    out_mal.loc[out_mal['demo_id'] == 35, 'demo_id'] = 'F:35-39'
    out_mal.loc[out_mal['demo_id'] == 40, 'demo_id'] = 'F:40-44'
    out_mal.loc[out_mal['demo_id'] == 45, 'demo_id'] = 'F:45-49'
    out_mal.loc[out_mal['demo_id'] == 50, 'demo_id'] = 'F:50-54'
    out_mal.loc[out_mal['demo_id'] == 55, 'demo_id'] = 'F:55-64'
    out_mal.loc[out_mal['demo_id'] == 65, 'demo_id'] = 'F:65+'
    out_mal = out_mal.groupby(['demo_id'])['UE'].sum()
    out_mal = out_mal.to_frame()
    out_mal.reset_index(inplace=True)
    
# Adding 100 to the demo_id for male demo_buckets
    out_mal['demo_id'] = (out_mal['demo_id'].str.replace("F:","M:")).astype(str)

# Concatenating male and female & rounding off UEs to nearest 100 to get the final output 
    result = pd.concat([out_fem, out_mal])

# Adding extra columns to prepare for the final csv outputs
    for_csv = pd.DataFrame([[country_id, x, y, 0, UE_start_date, UE_end_date, 'Pop total', 0]
                        for x,y in zip(result['demo_id'], result['UE'])])

# Exporting the output to .csv and .txt files
    for_csv.to_csv(csv_output_file, sep='|', header=False, index=False)

# Previous year file and check - just the result of QC
    compare, check = quality_check(csv_output_file, prev_yr_csv_file)
    compare.to_csv(compare_file, encoding='utf-8', index=False)

    return html.Div([
        html.Hr(),
        html.Hr(),
        html.H2(children='OUTPUT FILE',
                style={
                    'textAlign': 'center',
#                    'color': '#7FDBFF'
                }
                ),

        dash_table.DataTable(
            style_table={
                'width': '50%',
            },
            data=for_csv.to_dict('records'),
            columns=[{'name': str(i), 'id': str(i)} for i in for_csv.columns],
            style_cell={'padding': '10px',
                        'maxWidth': 0,
                        'height': 20,
                        'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'color': 'black'
            },
            style_cell_conditional=[],
            virtualization=True,
            export_format='xlsx',
            export_headers='display',

        ),
        html.Hr(),
        html.Hr(),
        html.H2(children='COMPARISON FILE',
                style={
                    'textAlign': 'center',
#                    'color': '#7FDBFF'
                }
                ),
        dash_table.DataTable(
            style_table={
                'width': '50%',
            },
            data=compare.to_dict('records'),
            columns=[{'name': str(i), 'id': str(i)} for i in compare.columns],
            style_cell={'padding': '10px',
                        'maxWidth': 0,
                        'height': 20,
                        'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'color': 'black'
            },
            style_cell_conditional=[],
            virtualization=True,

        ),
        html.Hr(),
        html.Hr(),
        html.H2(children='COMPARISON GRAPH CURR v/s PREV',
                style={
                    'textAlign': 'center',
#                    'color': '#7FDBFF'
                }
                ),        
        make_chart(pd.DataFrame(compare)),

        ])

#***************************************
# Function to prepare intermediate table 
#***************************************
def intermed (input_file, gender, in_column, age_groups):
    out_df = pd.DataFrame([[gender, x, 0] for x in age_groups], columns = ['Gender','Age_group','UE'])    
    for i,age in enumerate(age_groups):
        if '+' in age:
            start=int(age.split('+')[0])
            out_df['UE'][i]=in_column[start:len(in_column)].sum()
        else:
            start=int(age.split('-')[0])
            end=int(age.split('-')[1])
            if start==end:
                out_df['UE'][i]=in_column[start].sum()
            else:
                out_df['UE'][i]=in_column[start:(end+1)].sum()
    return out_df

#***************************************
# Function to prepare final table 
#***************************************      
def final(df, age_cat):
    out = pd.DataFrame([[x, 0] for x in sorted(age_cat.keys())],
                    columns = ['demo_id','UE'])
                    
    for d_id, demo_grp in age_cat.items():
        for cat in demo_grp:
            out.loc[out['demo_id'] == d_id, 'UE'] += \
            int(df.loc[df['Age_group'] == cat, 'UE'])
            
    return out
    
#******************
# Quality check
#******************
def quality_check(file1, file2):
    current = pd.read_csv(file1, sep='|', header=None, usecols = [1,2], names = ['demo_id', 'cur_UE'])
    previous = pd.read_csv(file2, sep='|', header=None, usecols = [1,2], names = ['demo_id', 'pre_UE'])
    compare = pd.merge(current, previous, on = 'demo_id', how = 'inner')   
    compare['per_diff'] = (compare['cur_UE'] - compare['pre_UE'])/compare['pre_UE'] *100
    compare['Index_of_dissimilarity'] = abs((compare['cur_UE']/sum(compare['cur_UE'])) 
                                        - (compare['pre_UE']/sum(compare['pre_UE'])))                                    
    compare['per_diff_gt3'] = 0
    compare['per_diff_gt6'] = 0
    compare.loc[((compare['demo_id'] == 65) | (compare['demo_id'] == 165)) & (abs(compare['per_diff']) > 4) , 'per_diff_gt3'] = 1
    compare.loc[((compare['demo_id'] != 65) & (compare['demo_id'] != 165)) & (abs(compare['per_diff']) > 3) , 'per_diff_gt3'] = 1
    compare.loc[(abs(compare['per_diff']) > 6) , 'per_diff_gt6'] = 1    
    compare.loc['check'] = 0    
    compare.loc['check','Index_of_dissimilarity'] = sum(compare['Index_of_dissimilarity']) \
                                                    * 0.5 * 100 < 3
    compare.loc['check','per_diff_gt3'] = sum(compare['per_diff_gt3']) < \
                                          0.1 * len(current.index)
    compare.loc['check','per_diff_gt6'] = sum(compare['per_diff_gt6']) == 0
    
    check = (compare.filter(items = ['Index_of_dissimilarity', 
                                    'per_diff_gt3',
                                    'per_diff_gt6'])).filter(like='check', axis=0)
    return compare, check

def make_chart(df):
    fig = px.histogram(df, x='demo_id' ,y='per_diff')
    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)
