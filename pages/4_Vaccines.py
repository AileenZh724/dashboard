

# import packages
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.cluster import KMeans
import numpy as np
import scipy as sp
from scipy import stats
#import seaborn as sns 
import plotly.express as px
import plotly.graph_objs as go

df_national_cum=pd.read_csv('P4_COVID_AU_national_cumulative.csv').fillna(0)
df_national_cum['date'] = df_national_cum['date'].apply(pd.to_datetime)
df_national_cum['vaccines']=df_national_cum['vaccines'].astype(int)
df_national_cum.set_index('date', inplace=True)

df_national_daily=pd.read_csv('P4_COVID_AU_national_daily_change.csv')
df_national_daily['date'] = df_national_daily['date'].apply(pd.to_datetime)
df_national_daily.set_index('date', inplace=True)

df_state_cum=pd.read_csv('COVID_AU_state_cumulative.csv').fillna(0)
df_state_cum['date'] = df_state_cum['date'].apply(pd.to_datetime)
df_state_cum['vaccines']=df_state_cum['vaccines'].astype(int)
df_state_cum.set_index('date', inplace=True)

df_state_daily=pd.read_csv('COVID_AU_state_daily_change.csv')
df_state_daily['date'] = df_state_daily['date'].apply(pd.to_datetime)
df_state_daily.set_index('date', inplace=True)


vacc_state = pd.read_csv("Total doses.csv")
vacc_state['date'] = pd.to_datetime(vacc_state['date'])


daily_vacc = pd.read_csv("National.csv")
daily_vacc['date'] = pd.to_datetime(daily_vacc['date'])
daily_vacc.info()

vacc_au=pd.read_csv('data-JallM.csv').fillna(0)
vacc_au['Date'] = vacc_au['Date'].apply(pd.to_datetime)
vacc_au['Actual 1st doses']=vacc_au['Actual 1st doses'].astype(float)
vacc_au['Actual 2nd doses']=vacc_au['Actual 2nd doses'].astype(float)
vacc_au['Actual Boosters']=vacc_au['Actual Boosters'].astype(float)
#vacc_au.set_index('Date', inplace=True)


per_vacc_au = px.line(vacc_au, x="Date", 
                    y=['Actual 1st doses','Actual 2nd doses','Actual Boosters'], 
                    title="Percentage of vaccines delivered in Australia",
                    labels={'value':'percentage of vaccines delivered',"variable":" "})
#per_vacc_au.update_layout(height=300, margin={'l': 20, 'b': 30, 'r': 40, 't': 40})

per_vacc_au.update_layout(
    #ylabel= 'percentage of vaccines delivered',
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=1
),
#height=460, margin={'l': 20, 'b': 30, 'r': 40, 't': 60}
)

per_vacc_au.show()


vacc_state=pd.read_csv('type_doses.csv').fillna(0)

vacc_state.info()


# ## left bottom graph


vacc_state.columns = vacc_state.columns.str.replace('state', 'state_abbrev')



vacc_state['state_abbrev'].unique()



vacc_state['state'] = vacc_state['state_abbrev'].replace(['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT'], 
                                                        ['New South Wales','Victoria',
                                                         'Queensland', 'South Australia', 'Western Australia','Tasmania',
                                                         'Northern Territory','Australian Capital Territory'])


import json
import requests
with open("statesgeo.json") as f:
    au_states = json.load(f)


import dash             #(version 1.8.0)
from dash.exceptions import PreventUpdate
from dash import Dash, html, dcc, Input, Output, callback
import IPython.display
from IPython.display import Image


# ## dashboard

# In[211]:


df_national_cum.loc[df_national_cum[df_national_cum['vaccines']<0].index, 'vaccines'] = 0
df_national_daily.loc[df_national_daily[df_national_daily['vaccines']<0].index, 'vaccines'] = 0
df_state_daily.loc[df_state_daily[df_state_daily['vaccines']<0].index, 'vaccines'] = 0
df_state_cum.loc[df_state_cum[df_state_cum['vaccines']<0].index, 'vaccines'] = 0


#

option=(vacc_state['category']).unique()


from datetime import date
from dash.dependencies import Input, Output
from datetime import datetime as dt
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__, external_stylesheets=external_stylesheets)

layout = html.Div([

    html.H3(
        children='Vaccines',
        style={
            'textAlign': 'center',
        }
    ),
#--------------------------download button------------------------------------------
    html.Div([
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-4")
    ],style={'float': 'right', 'display': 'inline-block'}),
#--------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
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
    html.Div(id='output-container-date-picker-range'),
        html.P("Select data type:"),
        dcc.RadioItems(
            ['Daily', 'Cumulative'],
            'Daily',
            id='daily_or_cum',
            labelStyle={'display': 'inline-block', 'marginTop': '5px','margin':'5px'}
        )
    ]),
#-------------------------------------------------------------------------------------------------
    html.Div(children=[
        #图片1
         dcc.Graph(
            id='graph_q',
            figure=per_vacc_au
            
        ),
        
#------------------------dropdown--------------------------------------------------------------------
        dcc.Dropdown(
            options=option,
            id='dropdown_option',
            placeholder='Select a value to view corresponding data on map: 3 doses 16+',
            style={'width': '85%'}
        ), 
#--------------------------------------------------------------------------------------------------------          
        #map
        dcc.Graph(
            id='graph_s',
            #figure=tree,
           
        )
        ],style={'width': '49%', 'display': 'inline-block'}),
#-----------------------------------------------------------------------------------------------------------------------
    #右半部分的图片
    html.Div([
        dcc.Graph(id='graph_t'),
        dcc.Graph(id='graph_u'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    dcc.Markdown('''
    Data Source: [www.covid19data.com.au](https://www.covid19data.com.au/vaccines)

    Tips: Use time range picker to change time length of x-aixs on some graphs. 
    
    Click the circle below time range picker to switch between daily and culmulative data.
''')
])


@callback(
    #Output('graph_q','figure'),
    #Output('graph_s','figure'),
    Output('graph_t','figure'),
    Output('graph_u','figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')],
    Input('daily_or_cum','value'))
def update_graph(start_date, end_date,datatype):
    if datatype=='Daily':
        dff_AU=df_national_daily.loc[start_date:end_date]
        dff_state=df_state_daily.loc[start_date:end_date]
        dff_n_doses = vacc_state.loc[start_date:end_date]
        fig3=px.bar(dff_AU,x=dff_AU.index,y='vaccines',title='Daily Vaccines delivered in Australia',
                            labels={'state_abbrev':'state',
                            'vaccines':'Number of vaccines delivered'})
        fig3.update_layout(height=465)
        fig4=px.bar(dff_state,x=dff_state.index,y='vaccines',color='state_abbrev',
                    labels={'state_abbrev':'state',
                            'vaccines':'Number of vaccines delivered'},
                    title='Daily Vaccines delivered by state')
        fig4.update_layout(
                                legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1,
                                xanchor="right",
                                x=1
                            ),
                            height=465
                            )
        

    else:
        dff_AU=df_national_cum.loc[start_date:end_date]
        dff_state=df_state_cum.loc[start_date:end_date]
        dff_n_doses = vacc_state.loc[start_date:end_date]
        fig3=px.line(dff_AU,x=dff_AU.index,y='vaccines',title='Cumulative Vaccines delivered in Australia',
                    labels={'state_abbrev':'state',
                    'vaccines':'Number of vaccines delivered'},)
        fig4=px.line(dff_state,x=dff_state.index,y='vaccines',color='state_abbrev',
                    labels={'state_abbrev':'state',
                            'vaccines':'Number of vaccines delivered'},
                    title='Cumulative Vaccines delivered by state')
        fig4.update_layout(
                                legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1,
                                xanchor="right",
                                x=1
                            )
                            )
        
    return fig3,fig4

#-------------------------download callback-------------------------------------------
@callback(
    Output("download-dataframe-4", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(daily_vacc.to_csv,'daily_vacc.csv')
#-------------------------------------------------------------------------------------
#------------------------------dropdown callback----------------------------------------
@callback(
    Output('graph_s', 'figure'),
    Input('dropdown_option', 'value')
)
def dropdown_changed(type_vairable):

    if type_vairable is not None:
        df_map = vacc_state.loc[vacc_state['category']==type_vairable]
        fig2=px.choropleth(
            df_map, 
            geojson=au_states,
            locations="state",
            featureidkey="properties.STATE_NAME",
            color="value",
            hover_name="state",
            hover_data=['category'],
            color_continuous_scale=px.colors.sequential.Plasma
        )
        fig2.update_geos(fitbounds="locations", visible=False)
        fig2.update_layout(
                                legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1,
                                xanchor="right",
                                x=1
                            )
                            )
        return fig2
#------------------------------------------------以下noerror----------------------------------------------------------------
    df_map = vacc_state.loc[vacc_state['category']=='3 doeses 16+']
    fig2=px.choropleth(
        df_map, 
        geojson=au_states,
        locations="state",
        featureidkey="properties.STATE_NAME",
        color="value",
        labels=({'value':'% of population'}),
        title='Percentage of adults vaccinated in each state',
        hover_name="state",
        hover_data=['category'],
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(
                            legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1,
                            xanchor="right",
                            x=1
                        )
                        )
    return fig2
#----------------------------------------------------------------------------------------------







