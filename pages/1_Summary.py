# import package
#import seaborn as sns
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.lines as pline
import plotly.express as px
import datetime
import dash
from dash import Dash, html, dcc, dash_table,callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], path='/')

df_national_cum=pd.read_csv('COVID_AU_national_cumulative.csv').fillna(0)
df_national_cum['date'] = df_national_cum['date'].apply(pd.to_datetime)
df_national_cum['tests']=df_national_cum['tests'].astype(int)
df_national_cum['positives']=df_national_cum['positives'].astype(int)

df_national_daily=pd.read_csv('COVID_AU_national_daily_change.csv')
df_national_daily['date'] = df_national_daily['date'].apply(pd.to_datetime)
df_national_daily['positive rate']=df_national_daily['positives']/df_national_daily['tests'].round(3)
df_national_daily['positive rate']=df_national_daily['positive rate'].fillna(0)
df_national_daily.replace([np.inf, -np.inf], 0, inplace=True)
for n in ['confirmed','tests']:
    for i in range(len(df_national_daily)):
        if df_national_daily.loc[i,n]<0:
            df_national_daily.loc[i,n]=-df_national_daily.loc[i,n]
df_national_daily.set_index('date', inplace=True)

df_state_cum=pd.read_csv('COVID_AU_state_cumulative.csv').fillna(0)
df_state_cum['date'] = df_state_cum['date'].apply(pd.to_datetime)
df_state_cum['tests']=df_state_cum['tests'].astype(int)
df_state_cum['positives']=df_state_cum['positives'].astype(int)

df_state_daily=pd.read_csv('COVID_AU_state_daily_change.csv')
df_state_daily['date'] = df_state_daily['date'].apply(pd.to_datetime)
for n in ['confirmed','tests']:
    for i in range(len(df_state_daily)):
        if df_state_daily.loc[i,n]<0:
            df_state_daily.loc[i,n]=-df_state_daily.loc[i,n]

df_totalcase_state= pd.read_csv('Total cases_state.csv')
df_totalcase_state['Date'] = df_totalcase_state['Date'].apply(pd.to_datetime)

df_total_death_state= pd.read_csv('deaths_cumulative_state_1month.csv')
df_total_death_state['Date'] = df_total_death_state['Date'].apply(pd.to_datetime)

def singleRow2ColByDate(df, date):
    '''
    convert row to col and drop row: 'Date'
    '''

    row = df[df['Date']==date]
    col = row.T
    col = col.drop('Date', axis = 0)

    return col
    
def stateDataGenerator(date):
    '''
    Given @param: date, generate a summary dataframe that 
    contains cases, percentage of all, #death 
    '''
    
    df_death = pd.read_csv('deaths_cumulative_state_1month.csv')
    df_death['Date'] = df_death['Date'].apply(pd.to_datetime)

    death_info = singleRow2ColByDate(df_death, date)

    summary = singleRow2ColByDate(df_totalcase_state, date)
    #summary = summary.drop('total', axis = 0)
    prev_name =  summary.columns[0]
    summary.rename(columns={prev_name: "Cases"}, inplace=True)
    summary['Cases']=summary['Cases'].astype('int')
    summary['% of all cases in Australia'] =(summary["Cases"] / summary["Cases"].sum()).round(3)
    summary['Death'] = death_info
    return summary

summary_state_2022_10_14 = stateDataGenerator('2022-10-14')
summary_state_2022_10_14.reset_index(inplace=True)
summary_state_2022_10_14= summary_state_2022_10_14.rename(columns={'index': 'State'}) 


y=2022
m=9
d=25
a = datetime.datetime(y, m, d)
b= datetime.datetime(y, m, d-6)
c=datetime.datetime(y, m, d-12)
#df_national_daily['confirmed'].loc[b:a,]
columns=['Last 7 days','Trend']
item=['positive rate','confirmed','deaths','tests','vaccines','hosp','icu']
#rows=['Positive rate', 'Total cases','Death', 'Total PRC tests conducted','Vaccine','Patient in hospital','Patient in ICU']
summury_national=pd.DataFrame(0, columns=columns, index=item) 
item=['positive rate','confirmed','deaths','tests','vaccines','hosp','icu']
for i in item:
    summury_national.loc[i,'Last 7 days']=df_national_daily[i].loc[b:a,].sum().round(3)
    if df_national_daily[i].loc[b:a,].sum()<df_national_daily[i].loc[c:b,].sum():
        summury_national.loc[i,'Trend']='decrease'
    elif df_national_daily[i].loc[b:a,].sum()>df_national_daily[i].loc[c:b,].sum():
        summury_national.loc[i,'Trend']='increase'
    else:
        summury_national.loc[i,'Trend']='stable'
summury_national  = summury_national .rename(index={'positive rate':'Positive rate','confirmed': 'Total cases','deaths':'Deaths','tests':'PCR test conducted','vaccines':'Vaccines','hosp':'Patients in hospital','icu':'Patients in ICU'})
summury_national.reset_index(inplace=True)
summury_national= summury_national.rename(columns={'index': 'Measures'}) 
#-----------------------------------------------------------------------dashboard----------------------------------------------------------------------------------
layout = html.Div([
    html.H3('Latest data summary (data updated on Sep 25)', style={'textAlign': 'center'}),
#----------------------------------------------------------------------------    
     html.Div([
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe_1")
    ],style={'float': 'right', 'display': 'inline-block'}),
#------------------------------------------------------------------------------
    
    dbc.Row([
        dbc.Col(
            html.Div(children=[
                html.H5('National data'),
                dash_table.DataTable(
                    id = 'table1',
                    data = summury_national.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in summury_national.columns],
                    style_header={ 'border': '1px solid black' },
                    style_cell={ 'border': '1px solid grey' },
                    style_table={'height': '500px'}
                    ),
                    dcc.Markdown('''Data Source: [www.covid19data.com.au] (https://www.covid19data.com.au/)''')
                    ]), 
            width=6),
        dbc.Col(
            html.Div([
                html.H5('State data'),
                dash_table.DataTable(
                    id = 'table2',
                    data = summary_state_2022_10_14.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in summary_state_2022_10_14.columns],
                    style_header={ 'border': '1px solid black' },
                    style_cell={ 'border': '1px solid grey' })
                    ]), 
            width=6)
    ])
])

#--------------------------------------------------------------------------------------------------
@callback(
    Output("download-dataframe_1", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True)
def func(n_clicks):
    return dcc.send_data_frame(df_national_daily.to_csv,'COVID_AU_national_daily_change.csv')
#-----------------------------------------------------------------------------------------------------


