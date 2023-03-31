import pandas as pd
import re
import dash

from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import stat 
from support_functions import taxonomy_distribution_table, taxonomy_distribution_barplot



#
df_all = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')




# Callback 1: Selecting search option
@callback(
    Output('search-dropdown', 'options'), 
    [
        Input('gcf-number', 'n_clicks'),
        Input('accession-number', 'n_clicks'),
        Input('node', 'n_clicks')
    ],
)

def update_dropdown_options(gcf_click=None, acc_click=None, node_click=None):
    df = df_netflax
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'gcf-number':
        options = list(set(df['gcf_number'].values.tolist()))  
    elif button_id == 'accession-number':
        options = list(set(pd.concat([df['at_accession'], df['t_accession']]).tolist()))
    elif button_id == 'node':
        options = list(set(pd.concat([df['at_domain'], df['t_domain']]).tolist()))
    else:
        options = []
    
    return [{'label': option, 'value': option} for option in options]



# Callback 2: Getting info about selected option
@callback(
    Output('result-container', 'children'), 
    Input('search-dropdown', 'value')
)

def search_results(search_term):
    if search_term.startswith('GCF'):
        number_of_ta = df_all.loc[df_all['gcf_number'] == search_term, 'number_of_predicted_tas'].values[0]
        proteome_size = df_all.loc[df_all['gcf_number'] == search_term, 'proteome_size'].values[0]
        term_superkingdom = df_all.loc[df_all['gcf_number'] == search_term, 'superkingdom'].values[0]
        term_phylum = df_all.loc[df_all['gcf_number'] == search_term, 'phylum'].values[0]
        term_class = df_all.loc[df_all['gcf_number'] == search_term, 'class'].values[0]
        term_order = df_all.loc[df_all['gcf_number'] == search_term, 'order'].values[0]
        term_family = df_all.loc[df_all['gcf_number'] == search_term, 'family'].values[0]
        term_genus = df_all.loc[df_all['gcf_number'] == search_term, 'genus'].values[0]
        term_species = df_all.loc[df_all['gcf_number'] == search_term, 'species'].values[0]
        term_subspecies = df_all.loc[df_all['gcf_number'] == search_term, 'taxa'].values[0]
        return html.Div(
            dbc.Row([
                html.H4(f'Search results for "{search_term}"')
            ]),
            dbc.Row([
                dbc.Col([

                ]),
                dbc.Col([

                ]),
            ])

        )
    elif search_term.startswith('WP_'):
        for row in df_netflax.itertuples():
            search_a = row['at_accession']
            search_t = row['t_accession']
    elif search_term.startswith('D') or search_term.startswith('M'):
        search_nod = search_term
    else:
        print(f'{search_term} not specified')



# # Callback 2: Selecting search option
# @callback(
#     Output('result-container', 'children'), 
#     Input('search-dropdown', 'value'),
# )

# def update_result_container(value):
#     if value:
#         # Show search results layout
#         return html.Div(
#             html.H4(f'Search results for "{value}"'),

#         )
#     else:
#         # Hide container if search is not initiated
#         return None


# Callback 3. Linking the Sunburst chart with the Taxonomy barplot
@callback(
    Output('a2_taxonomy_barplot', 'figure'),
    [
        Input('a1_superkingdom_sunburst', 'clickData'), 
        Input('phylum-level', 'n_clicks'),
        Input('class-level', 'n_clicks'),
        Input('order-level', 'n_clicks'),
        Input('family-level', 'n_clicks'),
        Input('genus-level', 'n_clicks')
    ]
)

def display_selected_kingdom(
    clickData, phylum_click=None, class_click=None,
    order_click=None, family_click=None, genus_click=None):

    # 1. Determine which kingdom was selected
    if clickData is not None:
        kingdom = clickData['points'][0]['label']
    else:
        kingdom = None
    
    # 2. Determine which taxonomy level button was clicked
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if button_id == 'phylum-level':
        level = 'phylum'
    elif button_id == 'class-level':
        level = 'class'
    elif button_id == 'order-level':
        level = 'order'
    elif button_id == 'family-level':
        level = 'family'
    elif button_id == 'genus-level':
        level = 'genus'
    else:
        level = 'phylum'
    
    # 3. Create the plots
    if kingdom is None:
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table('phylum', df_netflax, df_all), level)
    elif kingdom != None and kingdom == 'Total':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all), level)
    elif kingdom != None and kingdom == 'Bacteria_All':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all, 'Bacteria'), level)
    elif kingdom != None and kingdom == 'Archaea_All':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all, 'Archaea'), level)
    elif kingdom != None and kingdom == 'Viruses_All':
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table(level, df_netflax, df_all, 'Viruses'), level)
    else:
        bar_plot_data = taxonomy_distribution_barplot(taxonomy_distribution_table('phylum', df_netflax, df_all), level)
    
    return bar_plot_data
