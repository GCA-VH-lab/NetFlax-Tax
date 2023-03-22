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
from support_functions import sunburst, taxonomy_distribution_barplot, superkingdom_piechart, combinations_heatmap, taxonomy_distribution_table
# --------------------------- CREATE PAGE ------------------------------

dash.register_page(__name__, path = '/search')


df_all = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')


layout = html.Div([
            navigation.navbar,
            dbc.Row([

            ])               
        ])