import pandas as pd
import re
import dash

from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate



import stat 

df_all = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')





# Callback 1: Searchbar
def update_dropdown_options(btn_gcf, btn_acc, btn_node):
    data = df_netflax
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'gcf-number':
        return [{'label': value, 'value': value} for value in data['gcf_number']]
    elif button_id == 'accession-number':
        return [{'label': value, 'value': value} for value in data['at_accession']]
    elif button_id == 'node':
        return [{'label': value, 'value': value} for value in data['at_domain']]
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