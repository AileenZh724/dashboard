# import package
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as pline
import plotly.express as px
import datetime
import dash
from dash import Dash, html, dcc, dash_table,Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime as dt

external_stylesheets = external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash.register_page(__name__,external_stylesheets=external_stylesheets)

df_national_cum=pd.read_csv('COVID_AU_national_cumulative.csv').fillna(0)
df_national_cum['date'] = df_national_cum['date'].apply(pd.to_datetime)
df_national_cum['tests']=df_national_cum['tests'].astype(int)
df_national_cum['positives']=df_national_cum['positives'].astype(int)
df_national_cum.set_index('date', inplace=True)

df_national_daily=pd.read_csv('COVID_AU_national_daily_change.csv')
df_national_daily['date'] = df_national_daily['date'].apply(pd.to_datetime)
df_national_daily.set_index('date', inplace=True)
for i in ['confirmed','tests']:
    for n in df_national_daily.index:
        if df_national_daily.loc[n,i]<0:
            df_national_daily.loc[n,i]=-df_national_daily.loc[n,i]
        

df_state_cum=pd.read_csv('COVID_AU_state_cumulative.csv').fillna(0)
df_state_cum['date'] = df_state_cum['date'].apply(pd.to_datetime)
df_state_cum['tests']=df_state_cum['tests'].astype(int)
df_state_cum['positives']=df_state_cum['positives'].astype(int)
df_state_cum.set_index('date', inplace=True)

df_state_daily=pd.read_csv('COVID_AU_state_daily_change.csv')
df_state_daily['date'] = df_state_daily['date'].apply(pd.to_datetime)
for n in ['confirmed','tests']:
    for i in range(len(df_state_daily)):
        if df_state_daily.loc[i,n]<0:
            df_state_daily.loc[i,n]=-df_state_daily.loc[i,n]
df_state_daily.set_index('date', inplace=True)

df_totalcase_state= pd.read_csv('Total cases_state.csv')
df_totalcase_state['Date'] = df_totalcase_state['Date'].apply(pd.to_datetime)

df_total_death_state= pd.read_csv('deaths_cumulative_state_1month.csv')
df_total_death_state['Date'] = df_total_death_state['Date'].apply(pd.to_datetime)

layout = html.Div([
    html.H3('Cases and tests', style={'textAlign': 'center'}),
#----------------------------------------------------------------------------    
     html.Div([
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe_2")
    ],style={'float': 'right', 'display': 'inline-block'}),
#------------------------------------------------------------------------------    

    html.P("Select time range:"),
    #时间选项
    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        calendar_orientation='horizontal',  # vertical or horizontal
        day_size=39,  # size of calendar image. Default is 39
        end_date_placeholder_text="Return",  # text that appears when no end date chosen
        with_portal=False,  # if True calendar will open in a full screen overlay portal
        first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
        reopen_calendar_on_clear=True,
        is_RTL=False,  # True or False for direction of calendar
        clearable=True,  # whether or not the user can clear the dropdown
        number_of_months_shown=1,  # number of months shown when calendar is open
        min_date_allowed=dt(2020, 1, 5),  # minimum date allowed on the DatePickerRange component
        max_date_allowed=dt(2022, 9, 30),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=dt(2022, 7, 1),  # the month initially presented when the user opens the calendar
        start_date=dt(2022, 7, 1).date(),
        end_date=dt(2022, 9, 30).date(),
        display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
        minimum_nights=2,  # minimum number of days between start and end date
        persistence=True,
        persisted_props=['start_date'],
        persistence_type='session',  # session, local, or memory. Default is 'local'
        updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
    ),

    #Daily or cumulative
    html.P("Select data type:"),
    dcc.RadioItems(
                ['Daily', 'Cumulative'],
                'Daily',
                id='daily_or_cum',
                labelStyle={'display': 'inline-block', 'marginTop': '5px','margin':'5px'}),
      
    #图左上和左下(AUS)
    html.Div([
        dcc.Graph(id='cases-in-AU'),
        dcc.Graph(id='PRC-in-AU')   
    ],style={'display': 'inline-block', 'width': '49%'}),

    
    #图右上和右下(state)
    html.Div([
        dcc.Graph(id='cases-in-state'),
        dcc.Graph(id='PRC-in-state')
        ],style={'display': 'inline-block', 'width': '49%'}),
        #],style={'width': '99%','display': 'inline-block', 'padding': '0 20'}),
    dcc.Markdown('''
        Data Source: www.covid19data.com.au for [Tests](https://www.covid19data.com.au/testing) and [Cases](https://www.covid19data.com.au/states-and-territories) 

        Tips: Use time range picker to change time length of x-aixs on some graphs. 
        
        Click the circle below time range picker to switch between daily and culmulative data.
    ''')
])


@callback(
    Output('cases-in-AU','figure'),
    Output('PRC-in-AU','figure'),
    Output('cases-in-state','figure'),
    Output('PRC-in-state','figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')],
    Input('daily_or_cum','value'))
def update_graph(start_date, end_date,datatype):
    if datatype=='Daily':
        dff_AU=df_national_daily.loc[start_date:end_date]
        dff_state=df_state_daily.loc[start_date:end_date]
        fig1=px.bar(dff_AU,x=dff_AU.index,y='confirmed',title="Daily confirmed cases in AUS")
        fig1.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig2=px.bar(dff_AU,x=dff_AU.index,y='tests',title='Daily PRC test in AUS')
        fig2.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig3=px.bar(dff_state,x=dff_state.index,y='confirmed',color='state_abbrev',title='Daily confirmed cases in each state',labels={'state_abbrev':'state'})
        fig3.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig4=px.bar(dff_state,x=dff_state.index,y='tests',color='state_abbrev',title='Daily PRC test in each state',labels={'state_abbrev':'state'})
        fig4.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
    else:
        dff_AU=df_national_cum.loc[start_date:end_date]
        dff_state=df_state_cum.loc[start_date:end_date]
        fig1=px.line(dff_AU,x=dff_AU.index,y='confirmed',title="Cumulative confirmed cases in AUS")
        fig1.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig2=px.line(dff_AU,x=dff_AU.index,y='tests',title='Cumulative PRC test in AUS')
        fig2.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig3=px.line(dff_state,x=dff_state.index,y='confirmed',color='state_abbrev',title='Cumulative confirmed cases in each state',labels={'state_abbrev':'state'})
        fig3.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig4=px.line(dff_state,x=dff_state.index,y='tests',color='state_abbrev',title='Cumulative PRC test in each state',labels={'state_abbrev':'state'})
        fig4.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
    
    return fig1,fig2,fig3,fig4
#--------------------------------------------------------------------------------------------------
@callback(
    Output("download-dataframe_2", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True)
def func(n_clicks):
    return dcc.send_data_frame(df_totalcase_state.to_csv,'COVID_AU_total_case.csv')
#-----------------------------------------------------------------------------------------------------


