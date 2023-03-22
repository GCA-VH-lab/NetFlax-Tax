# ------------------------------- IMPORTS ------------------------------
import pandas as pd
import re
import dash

from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go
from plotly.subplots import make_subplots


from pages import navigation
from support_functions import sunburst, taxonomoy_barplot, superkingdom_piechart, combinations_heatmap
# --------------------------- CREATE PAGE ------------------------------

dash.register_page(__name__, path = '/search')


# df_all = pd.read_excel('/Users/veda/Dropbox (Personal)/NetFlax/Stats_App/Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='2. All_Searched_Data')
# df_netflax = pd.read_excel('/Users/veda/Dropbox (Personal)/NetFlax/Stats_App/Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='3. NetFlax_Data')
df_all = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='2. All_Searched_Data')
df_netflax = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='3. NetFlax_Data')
df_graph_2 = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='Graph_2')
df_netflax.drop(df_netflax[df_netflax['T Domain'] == 'D41'].index, inplace = True)




layout = html.Div([
            navigation.navbar,
            dbc.Row([

            ])               
        ])