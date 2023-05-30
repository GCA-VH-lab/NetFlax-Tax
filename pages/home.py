# LAYOUT OF FRONT PAGE

# Packages
import pandas as pd
import re
import dash

from dash import html, dcc, callback, ctx, dash_table
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Import data
from data.data_prep import *

# Import interactivity 
from callbacks import update_sunburst_level

# Import specifics
from pages import navigation
from assets.color_scheme import *



# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/')



# ------------------------------ LAYOUT --------------------------------

layout = html.Div([
    navigation.navbar,
    html.Div(id='error-message', className='error-message'),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id = 'a1_taxonomy_sunburst',
                    figure = update_sunburst_level()[0],
                    style = {
                        'width': '100%', 
                        'height': '100%', 
                        'justify-content': 'center',
                        'backgroundColor': transparent_background
                    }
                ),
                dbc.Row([
                    html.H5('Taxonomic Level'),
                    html.Div([
                            dcc.Slider(
                                id='taxonomy_level_slider',
                                min=0,
                                max=6,
                                step=1,
                                value=3,
                                marks={
                                    0: {'label': 'Superkingdom'},
                                    1: {'label': 'Phylum'},
                                    2: {'label': 'Class'},
                                    3: {'label': 'Order'},
                                    4: {'label': 'Family'},
                                    5: {'label': 'Genus'},
                                    6: {'label': 'Species'}
                                }
                            ),
                    ], style={
                        'width': '80%', 
                        'margin': 'auto',
                        'background': container_background
                    })
                ], style = {'background': container_background})
            ],  width={
                    'size': 7,
                    'offset': 0
            },  style={'height': '90vh', 'background': container_background}),
            dbc.Col(width={'size': 1}),
            dbc.Col([
                html.H3('Result output'),
                dbc.Row([
                    html.Div([
                        dbc.Button('Taxonomy', id = 'taxonomy', className = 'me-1', color = 'primary', outline = True),
                        dbc.Button('Accession Number', id = 'accession-number', className = 'me-1', color = 'primary', outline = True),
                        dbc.Button('Node', id = 'node', className = 'me-1', color = 'primary', outline = True),
                    ], style = {'padding': '10px'})
                ]),
                dbc.Row([
                    dcc.Loading(
                        dcc.Dropdown(
                            id = 'search-dropdown',
                            placeholder = 'Select a search option',
                            clearable = True
                        ),
                        type = 'default'
                    )
                ]),
                dbc.Row([
                    dcc.Loading(
                        id='result-container-loading', 
                        type='circle', 
                        fullscreen = True, 
                        children = [
                            html.Div(
                                id = 'results-container', 
                                style = {
                                    'textAlign': 'center',
                                    'padding': '10px',
                                    'justify-content': 'center',
                                })
                    ])
                ]), 
            ],  width={
                    'size': 4, 
                    'offset': 0}, 
                style={
                    'height': '90vh', 
                    'background': container_background,
                    'padding': '10px'}),
        ]),
    ], style={
        'backgroundColor': page_background,
        'padding': '60px'})
])






