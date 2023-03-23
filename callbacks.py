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

from support_functions import taxonomy_distribution_table, taxonomy_distribution_barplot



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


# @callback(
#     Output('search-results', 'children'),
#     Input('search-dropdown', 'value'),
# )
# def update_search_results(value):
#     if value is None:
#         return ''
#     return f'You searched for: {value}'



# 1. Linking the Sunburst chart with the Taxonomy barplot
@callback(
    Output(component_id='a2_taxonomy_barplot', component_property='figure'),
    [
        Input(component_id='a1_superkingdom_sunburst', component_property='clickData'), 
        Input(component_id='phylum-level', component_property='n_clicks'),
        Input(component_id='class-level', component_property='n_clicks'),
        Input(component_id='order-level', component_property='n_clicks'),
        Input(component_id='family-level', component_property='n_clicks'),
        Input(component_id='genus-level', component_property='n_clicks')
    ]
)
def display_selected_kingdom(
    clickData=None, phylum_click=None, class_click=None,
    order_click=None, family_click=None, genus_click=None):

    # 1. Deterimne which kingdom was selected
    if clickData is not None:
        kingdom = clickData['points'][0]['label']
    else:
        kingdom = None
    
    # 2. Determine which taxonomy level button was clicked
    buttons = [phylum_click, class_click, order_click, family_click, genus_click]
    if buttons != None:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'phylum-level':
            level = 'phylum'
        elif button_id == 'class-button':
            level = 'class'
        elif button_id == 'order-button':
            level = 'order'
        elif button_id == 'family-button':
            level = 'family'
        elif button_id == 'genus-button':
            level = 'genus'
        else:
            level = None
    
    # 3. Create the plots
    if kingdom == None and level == None:
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table('phylum', df_netflax, df_all))
    elif clickData != None and kingdom == 'Total':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all))
    elif clickData != None and kingdom == 'Bacteria_All':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all, 'Bacteria'))
    elif clickData != None and kingdom == 'Archaea_All':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all, 'Archaea'))
    elif clickData != None and kingdom == 'Viruses_All':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all, 'Viruses'))

    return bar_plot_data
