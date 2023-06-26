

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc



hos = pd.read_csv('COVID_AU_national.csv')
hos2 = pd.read_csv('COVID_AU_state.csv')



hos['date']=pd.to_datetime(hos['date'])
hos2['date']=pd.to_datetime(hos2['date'])


hos2.isnull().sum()


#import plotly.dashboard_objs as dashboard
from dash import Dash, html, dcc, Input, Output, callback
import IPython.display
from IPython.display import Image
#from chart_studio import plotly
import plotly.graph_objs as go
#import plotly.plotly as py
import plotly.express as px


hos.set_index('date', inplace=True)
hos2.set_index('date', inplace=True)

from datetime import date
from dash.dependencies import Input, Output
from datetime import datetime as dt
import dash

external_stylesheets = external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash.register_page(__name__,external_stylesheets=external_stylesheets)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([
    html.H3(
        children='Hospitalization',
        style={
            'textAlign': 'center',
        }
    ),
#--------------------------download button------------------------------------------
    html.Div([
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-5")
    ],style={'float': 'right', 'display': 'inline-block'}),
#--------------------------------------------------------------------------------------

    html.Div(children=[
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
        updatemode='singledate' # singledate or bothdates. Determines when callback is triggered
    ),
    
    html.Div(
        dbc.Row([
        dbc.Col(
            html.Div([html.P("Select data type:"),
                dcc.RadioItems(
            ['Daily', 'Cumulative'],
            'Daily',
            id='daily_or_cum')]),width=6),
        dbc.Col(
            html.Div([html.P("Select data type:"),
                dcc.Dropdown(
                ['National','State'],
                'National',
                id='filter-dropdown')]),width=6)])),
    html.Div(
        #image 1
        dcc.Graph(
            id='graph_v'
            
        ),style={'width': '49%', 'display': 'inline-block','margin': '25px 0px 0px 0px','padding':'0 10px'}),
    #image 2 and 3
    html.Div([
        dcc.Graph(id='graph_w'),
        dcc.Graph(id='graph_x'),
    ], style={'display': 'inline-block', 'width': '49%','margin': '25px 0px 0px 0px'}),
    dcc.Markdown('''
    Data Source: [www.covid19data.com.au](https://www.covid19data.com.au/hospitalisations-icu)
    
    Tips: Use time range picker to change time length of x-aixs on some graphs. 
    
    Click the circle below time range picker to switch between daily and culmulative data.

    Click the box above to Daily & Cumulative to switch between National and State data.
''')
])])



@callback(
    Output('graph_v','figure'),
    Output('graph_w','figure'),
    Output('graph_x','figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')],
    Input('daily_or_cum','value'),
    Input('filter-dropdown', 'value'))
def update_graph(start_date, end_date,datatype1,datatype2):
    if datatype1=='Daily' and datatype2=='National':
        hos_AU=hos.loc[start_date:end_date]
    
        fig1=px.bar(hos_AU,x=hos_AU.index,y='hosp',title="Daily COVID-19 cases in hospital")
        fig1.update_layout(height=520,margin={'l': 40, 'b': 40, 'r': 0, 't': 60},hovermode='closest')
        fig2=px.bar(hos_AU,x=hos_AU.index,y='icu',title='Daily COVID-19 cases in ICU')
        fig2.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 30})
        fig3=px.bar(hos_AU,x=hos_AU.index,y='vent',title='Daily COVID-19 cases on a ventilator')
        fig3.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 30})
    elif datatype1=='Cumulative' and datatype2=='National':
        hos_AU=hos.loc[start_date:end_date]
        
        fig1=px.line(hos_AU,x=hos_AU.index,y='hosp_cum',title="Cumulative COVID-19 cases in hospital")
        fig1.update_layout(height=520,margin={'l': 40, 'b': 40, 'r': 0, 't': 60})
        fig2=px.line(hos_AU,x=hos_AU.index,y='icu_cum',title='Cumulative COVID-19 cases in ICU')
        fig2.update_layout(height=250, margin={'l': 40, 'b': 40, 'r': 0, 't': 60})
        fig3=px.line(hos_AU,x=hos_AU.index,y='vent_cum',title='Cumulative COVID-19 cases on a ventilator')
        fig3.update_layout(height=250, margin={'l': 40, 'b': 40, 'r': 0, 't': 60})
    elif datatype1=='Daily' and datatype2=='State':
        hos_state=hos2.loc[start_date:end_date]
        
        fig1=px.bar(hos_state,x=hos_state.index,y='hosp',color = 'state',title="Daily COVID-19 cases in hospital")
        fig1.update_layout(height=520,margin={'l': 40, 'b': 40, 'r': 0, 't': 60},hovermode='closest')
        fig2=px.bar(hos_state,x=hos_state.index,y='icu',color = 'state',title='Daily COVID-19 cases in ICU')
        fig2.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 60})
        fig3=px.bar(hos_state,x=hos_state.index,y='vent',color = 'state',title='Daily COVID-19 cases on a ventilator')
        fig3.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 60})
    else:
        hos_state=hos2.loc[start_date:end_date]
        
        fig1=px.line(hos_state,x=hos_state.index,y='hosp_cum',color = 'state',title="Cumulative COVID-19 cases in hospital")
        fig1.update_layout(height=520,margin={'l': 40, 'b': 40, 'r': 0, 't': 60},hovermode='closest')
        fig2=px.line(hos_state,x=hos_state.index,y='icu_cum',color = 'state',title='Cumulative COVID-19 cases in ICU')
        fig2.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 60})
        fig3=px.line(hos_state,x=hos_state.index,y='vent_cum',color = 'state',title='Cumulative COVID-19 cases on a ventilator')
        fig3.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 60})
        
    return fig1,fig2,fig3


#-------------------------download callback-------------------------------------------
@callback(
    Output("download-dataframe-5", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(hos.to_csv,'COVID_AU_national.csv')
#-------------------------------------------------------------------------------------




