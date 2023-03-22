#!/bin/env python3


# This script generates the FlaGs graphical output with imporved interactivity 
# where the user can filter, select, click, and get more info about the data. 
#
# Run the applicatuib with 'python app.py' and visit 
# http://127.0.0.1:8050/ in your web browser.


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

dash.register_page(__name__, path = '/')


# df_all = pd.read_excel('/Users/veda/Dropbox (Personal)/NetFlax/Stats_App/Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='2. All_Searched_Data')
# df_netflax = pd.read_excel('/Users/veda/Dropbox (Personal)/NetFlax/Stats_App/Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='3. NetFlax_Data')
df_all = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='2. All_Searched_Data')
df_netflax = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='3. NetFlax_Data')
df_graph_2 = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='Graph_2')
df_netflax.drop(df_netflax[df_netflax['T Domain'] == 'D41'].index, inplace = True)

data = df_netflax

background_color = '#d2e0eb'
banner_color = '#c2cfda'


# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
            navigation.navbar,
            dbc.Row([
                html.Div(
                    html.H1(
                        'Search',
                        style = {
                            'writingMode': 'vertical-rl',
                            'transform': 'rotate(180deg)',
                            'height': '100px',
                            'width': '100px',
                            'textAlign': 'center',
                            'fontSize': '15px',
                        }),
                    style={
                        'backgroundColor': banner_color,
                        'height': '100%',
                        'width': '30px',
                        'position': 'fixed',
                        'top': 60,
                        'left': 5,
                        'padding': '5px',
                    }, id = 'banner_1'
                ),
                dbc.Row([
                    html.Div([
                        html.Button('Genome Assembly', id = 'gcf-number'),
                        html.Button('Accession Number', id = 'accession-number'),
                        html.Button('Node', id = 'node'),
                    ]),
                ], style={
                    'marginTop': '20px',
                    'marginLeft': '55px', 
                    'padding': '10px',
                    'backgroundColor': background_color}),
                dbc.Col([
                    dcc.Dropdown(
                        id = 'search-dropdown',
                        options = [{'label': k, 'value': k} for k in data.keys()],
                        placeholder = 'Search...',
                        clearable = True
                    ),
                ], style={
                    'marginTop': '5px',
                    'marginLeft': '55px', 
                    'padding': '10px',
                    'backgroundColor': background_color}),
                dbc.Col([
                    html.Div(
                        id = 'search-results'
                    )
                ])
            ]),
            dbc.Row([
                html.Div(
                    html.H1(
                        'Data Overview',
                        style = {
                            'writingMode': 'vertical-rl',
                            'transform': 'rotate(180deg)',
                            'height': '100px',
                            'width': '100px',
                            'textAlign': 'center',
                            'fontSize': '15px',
                        }),
                    style={
                        'backgroundColor': banner_color,
                        'height': '100%',
                        'width': '30px',
                        'position': 'fixed',
                        'top': 70,
                        'left': 5,
                        'padding': '5px',
                    }, id='banner_2'
                ),
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            id = 'a1_superkingdom_sunburst',
                            figure = sunburst(df_all), 
                        )
                    ], style={
                        'marginTop': '40px',
                        'marginLeft': '40px', 
                        'padding': '10px',
                        'backgroundColor': background_color},
                    )
                ], width = 5),
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            id = 'a2_taxonomy_barplot',
                            figure = taxonomoy_barplot(df_graph_2)
                        )
                    ], style={
                        'marginTop': '40px',
                        'marginLeft': '10px',
                        'marginRight': '10px', 
                        'padding': '10px',
                        'backgroundColor': background_color}),
                ], width = 7),
            ]),
            html.Br(),
            dbc.Row([
                html.Div(
                    html.H1(
                        'TA pairs',
                        style = {
                            'writingMode': 'vertical-rl',
                            'transform': 'rotate(180deg)',
                            'height': '100px',
                            'width': '100px',
                            'textAlign': 'center',
                            'fontSize': '15px',
                        }),
                    style={
                        'backgroundColor': banner_color,
                        'height': '90vh',
                        'width': '30px',
                        'position': 'fixed',
                        'left': 5,
                        'padding': '5px',
                    },
                ),
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            id = 'b1_combinations_sunburst',
                            figure = superkingdom_piechart(df_netflax)
                        )
                    ], style={
                        'marginTop': '40px',
                        'marginLeft': '40px',
                        'marginRight': '10px', 
                        'padding': '10px',
                        'backgroundColor': background_color})
                ], width = 5),
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            id = 'b2_combinations_heatmap',
                            figure = combinations_heatmap(df_netflax)
                        )
                    ], style={
                        'marginTop': '40px',
                        'marginLeft': '10px',
                        'marginRight': '10px', 
                        'padding': '10px',
                        'backgroundColor': background_color}),
                ], width = 7),
            ]),       
        ])




@callback(
    Output('search-results', 'children'),
    [Input('search-bar', 'value')]
)
def update_search_results(query):
    # perform search and return results as HTML
    if query:
        # perform search
        results = perform_search(query)
        
        # format results as HTML
        return html.Ul([
            html.Li(result) for result in results
        ])
    else:
        return html.Div()