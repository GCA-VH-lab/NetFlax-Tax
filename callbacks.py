import pandas as pd
import re
import dash

from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate



import stat 

df_all = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='2. All_Searched_Data')
df_netflax = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='3. NetFlax_Data')
df_graph_2 = pd.read_excel('./Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='Graph_2')
df_netflax.drop(df_netflax[df_netflax['T Domain'] == 'D41'].index, inplace = True)



# Callback 1: Searchbar

def update_dropdown_options(btn_gcf, btn_acc, btn_node):
    data = df_netflax
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'gcf-number':
        return [{'label': value, 'value': value} for value in data['GCF Number']]
    elif button_id == 'accession-number':
        return [{'label': value, 'value': value} for value in data['AT Accession']]
    elif button_id == 'node':
        return [{'label': value, 'value': value} for value in data['AT Domain']]
    else:
        return []


@callback(
    Output('search-results', 'children'),
    Input('search-dropdown', 'value'),
)
def update_search_results(value):
    if value is None:
        return ''
    return f'You searched for: {value}'