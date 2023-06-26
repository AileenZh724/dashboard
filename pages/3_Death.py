#!/usr/bin/env python
# coding: utf-8

# Deaths from covid in au
# Deaths by age and gender
# Deaths by state
# deaths 7-day average

# # Deaths from covid in au


# import packages
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

death_daily_au = pd.read_csv("deaths_daily_aus.csv")
death_daily_au['Date'] = pd.to_datetime(death_daily_au['Date'])


import itertools 
#AUS
cumu_aus = []
accum_aus = itertools.accumulate(death_daily_au['New deaths / day'])

for L in accum_aus:
    cumu_aus.append(L)
death_daily_au['Cumulative deaths_aus'] = cumu_aus


#NSW
cumu_nsw = []
accum_nsw = itertools.accumulate(death_daily_au['NSW'])

for n in accum_nsw:
    cumu_nsw.append(n)
death_daily_au['Cumulative deaths_nsw'] = cumu_nsw

#VIC
cumu_vic = []
accum_vic = itertools.accumulate(death_daily_au['VIC'])

for v in accum_vic:
    cumu_vic.append(v)
death_daily_au['Cumulative deaths_vic']= cumu_vic


#QLD
cumu_qld = []
accum_qld = itertools.accumulate(death_daily_au['QLD'])
for q in accum_qld:
    cumu_qld.append(q)
death_daily_au['Cumulative deaths_qld']=cumu_qld


#SA
cumu_sa = []

accum_sa = itertools.accumulate(death_daily_au['SA'])
for s in accum_sa:
    cumu_sa.append(s)
death_daily_au['Cumulative deaths_sa']=cumu_sa

#WA
cumu_wa = []
accum_wa = itertools.accumulate(death_daily_au['WA'])
for w in accum_wa:
    cumu_wa.append(w)
death_daily_au['Cumulative deaths_wa']= cumu_wa

#TAS
cumu_tas = []
accum_tas = itertools.accumulate(death_daily_au['TAS'])
for t in accum_tas:
    cumu_tas.append(t)
death_daily_au['Cumulative deaths_tas']=cumu_tas
#NT
cumu_nt = []
accum_nt = itertools.accumulate(death_daily_au['NT'])
for i in accum_nt:
    cumu_nt.append(i)
death_daily_au['Cumulative deaths_nt']= cumu_nt
#ACT
cumu_act = []
accum_act = itertools.accumulate(death_daily_au['ACT'])
for a in accum_act:
    cumu_act.append(a)
death_daily_au['Cumulative deaths_act']= cumu_act


#import plotly.dashboard_objs as dashboard
from dash import Dash, html, dcc, Input, Output,callback
import IPython.display
from IPython.display import Image
#from chart_studio import plotly
import plotly.graph_objs as go
#import plotly.plotly as py
import plotly.express as px



state_daily = px.bar(death_daily_au, x="Date", y=['NSW', 'VIC','QLD','SA','WA','TAS','NT','ACT'], title="Deaths from COVID-19 by state")



death_daily_au.columns



cum_line_state = px.line(death_daily_au, x="Date", y=['Cumulative deaths_nsw',
       'Cumulative deaths_vic', 'Cumulative deaths_qld',
       'Cumulative deaths_sa', 'Cumulative deaths_wa', 'Cumulative deaths_tas',
       'Cumulative deaths_nt', 'Cumulative deaths_act'], title='Cumulative Deaths from COVID-19 in Australia by state')




cum_line = px.line(death_daily_au, x="Date", y="Cumulative deaths_aus", title='Cumulative Deaths from COVID-19 in Australia')


his_daily_death = px.bar(death_daily_au, x="Date", y="New deaths / day", title='Deaths from COVID-19 in Australia')
#py.iplot(his_daily_death, filename='histogram_daily_deaths')



from pandas import Series, DataFrame
death_age_gender_total = {'Age Group':['0-39','40-49','50-59','60-69','70-79','80-89','90+'],
                            'Males':[41,67,187,466,1225,2022,1292],
                            'Females':[23,42,109,245,637,1482,1590]
                        }
death_age_gender_total = DataFrame(death_age_gender_total)
age_gender_bar = px.bar(death_age_gender_total, x='Age Group', y=['Males','Females'],title="Deaths from COVID-19 by age group and sex")
age_gender_bar.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})

death_daily_au[ '7day_rolling_avg' ] = death_daily_au['New deaths / day'].rolling( 7).mean().round(0)

avg_line = px.line(death_daily_au, x="Date", y="7day_rolling_avg", title='COVID-19 associated deaths, rolling 7-day average')



df_national_cum=pd.read_csv('COVID_AU_national_cumulative.csv').fillna(0)
df_national_cum['date'] = df_national_cum['date'].apply(pd.to_datetime)
df_national_cum['deaths']=df_national_cum['deaths'].astype(int)
df_national_cum['vaccines']=df_national_cum['vaccines'].astype(int)
df_national_cum.set_index('date', inplace=True)

df_national_daily=pd.read_csv('COVID_AU_national_daily_change.csv')
df_national_daily['date'] = df_national_daily['date'].apply(pd.to_datetime)
df_national_daily.set_index('date', inplace=True)

df_state_cum=pd.read_csv('COVID_AU_state_cumulative.csv').fillna(0)
df_state_cum['date'] = df_state_cum['date'].apply(pd.to_datetime)
df_state_cum['deaths']=df_state_cum['deaths'].astype(int)
df_state_cum['vaccines']=df_state_cum['vaccines'].astype(int)
df_state_cum.set_index('date', inplace=True)

df_state_daily=pd.read_csv('COVID_AU_state_daily_change.csv')
df_state_daily['date'] = df_state_daily['date'].apply(pd.to_datetime)
df_state_daily.set_index('date', inplace=True)

df_total_death_state= pd.read_csv('deaths_cumulative_state_1month.csv')
df_total_death_state['Date'] = df_total_death_state['Date'].apply(pd.to_datetime)

death_daily_au['7day_rolling_avg']=death_daily_au['7day_rolling_avg'].fillna(0)
death_daily_au['7day_rolling_avg']=death_daily_au['7day_rolling_avg'].astype(int)
death_daily_au.set_index('Date', inplace=True)



death_daily_au['7day_rolling_avg']=death_daily_au['7day_rolling_avg'].fillna(0)



from datetime import date
from dash.dependencies import Input, Output
from datetime import datetime as dt
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__, external_stylesheets=external_stylesheets)

layout = html.Div([
    html.H3(
        children=
        'Deaths',
        style={
            'textAlign': 'center',
        }
    ),
#--------------------------download button------------------------------------------
    html.Div([
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-3")
    ],style={'float': 'right', 'display': 'inline-block'}),
#--------------------------------------------------------------------------------------

    html.Div(children=[
    
    
    #时间选项
    html.P("Select time range:"),
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
        updatemode='singledate' # singledate or bothdates. Determines when callback is triggered
    ),
    html.Div(id='output-container-date-picker-range'),
        html.P("Select data type:"),
        dcc.RadioItems(
            ['Daily', 'Cumulative'],
            'Daily',
            id='daily_or_cum',
            labelStyle={'display': 'inline-block', 'marginTop': '-2px','margin':'5px'}
        )
    ]),

    html.Div(children=[
        #图片1
        dcc.Graph(
            id='graph_l'
            
        ),
        #图2
        dcc.Graph(
            id='graph_m',
            
            style={'color':'#ded9d9'}
        )
    ],style={'width': '50%', 'display': 'inline-block'}),
    #右半部分的图片
    html.Div([
        dcc.Graph(id='graph_n', figure= age_gender_bar),
        dcc.Graph(id='graph_o'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    dcc.Markdown('''
        Data Source: [www.covid19data.com.au](https://www.covid19data.com.au/deaths)

        Tips: Use time range picker to change time length of x-aixs on some graphs. 
        
        Click the circle below time range picker to switch between daily and culmulative data.
    ''')
])


@callback(
    Output('graph_l','figure'),
    Output('graph_m','figure'),
    Output('graph_o','figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')],
    Input('daily_or_cum','value'))
def update_graph(start_date, end_date,datatype):
    if datatype=='Daily':
        dff_AU=df_national_daily.loc[start_date:end_date]
        dff_state=df_state_daily.loc[start_date:end_date]
        dff_7avg = death_daily_au.loc[start_date:end_date]
    
        fig1=px.bar(dff_AU,x=dff_AU.index,y='deaths',title="Deaths from COVID-19 in Australia")
        fig1.update_layout(
            height=460, 
            margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig2=px.bar(dff_state,x=dff_state.index,y='deaths',color='state_abbrev',title='Deaths from COVID-19 by state',labels={'state_abbrev':'state'})
        fig2.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig3=px.line(dff_7avg,x=dff_7avg.index,y='7day_rolling_avg',title='COVID-19 associated, rolling 7-day average')
        fig3.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
    else:
        dff_AU=df_national_cum.loc[start_date:end_date]
        dff_state=df_state_cum.loc[start_date:end_date]
        dff_7avg = death_daily_au.loc[start_date:end_date]

        fig1=px.line(dff_AU,x=dff_AU.index,y='deaths',title="Cumulative deaths in AUS")
        fig1.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig2=px.line(dff_state,x=dff_state.index,y='deaths',color='state_abbrev',title='Cumulative deaths in AUS by state',labels={'state_abbrev':'state'})
        fig2.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
        fig3=px.line(dff_7avg,x=dff_7avg.index,y='7day_rolling_avg',title='COVID-19 associated, rolling 7-day average')
        fig3.update_layout(height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})
    return fig1,fig2,fig3
    
#-------------------------download callback-------------------------------------------
@callback(
    Output("download-dataframe-3", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(death_daily_au.to_csv,'deaths_daily_aus.csv')
#-------------------------------------------------------------------------------------





