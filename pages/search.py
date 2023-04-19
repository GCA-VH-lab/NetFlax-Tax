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
from support_functions import taxonomy_sunburst, sunburst

from callbacks import update_sunburst_level
# --------------------------- CREATE PAGE ------------------------------

dash.register_page(__name__, path = '/search')


df_all = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')


layout = html.Div([
            navigation.navbar,
            dbc.Row([
                html.H1('Something Something'),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H3('Taxonomy Sunburst'),
                    dcc.Graph(
                        id = 'a1_taxonomy_sunburst',
                        figure = sunburst(),
                        style = {'width': '100%', 'height': '100%'}
                            ),
                    html.Br(),
                    html.H5('Taxonomic Level'),
                    # dcc.Slider(
                    #     id = 'taxonomy_level_slider',
                    #     min = 0,
                    #     max = 6,
                    #     step = 1,
                    #     value = 3,
                    #     marks={
                    #         0: {'label': 'Superkingdom'},
                    #         1: {'label': 'Phylum'},
                    #         2: {'label': 'Class'},
                    #         3: {'label': 'Order'},
                    #         4: {'label': 'Family'},
                    #         5: {'label': 'Genus'},
                    #         6: {'label': 'Species'}
                    #     }
                    # )
                ], width={'size': 8, 'offset': 0}, style={'height': '90vh'}),
                dbc.Col([
                    html.Br(),
                    html.H3('Result output')
                ], width={'size': 4, 'offset': 0}, style={'height': '90vh'}),         
            ])      
        ])






