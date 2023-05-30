import pandas as pd
import re
import dash
import requests

import plotly.express as px
from dash import html, dcc, callback, ctx, dash_table
from dash.dependencies import Input, Output, State

import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_cytoscape as cyto


import stat 
from support_functions import taxonomy_distribution_table, taxonomy_distribution_barplot
from test_protein_viewer import structure_file, get_structural_data, create_mol3d_style


df_all = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')




# ---------------------------- CALLBACKS -------------------------------


# Callback 2: Getting info about selected option
@callback(
    Output('result-container', 'children'), 
    Input('search-dropdown', 'value'),
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
        part_of_netflax = "Yes" if number_of_ta > 0 else "No"
        return html.Div(
            children=[
                dbc.Row([
                    html.H4(f'Search results for "{search_term}"')
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(title=f'Superkingdom: {term_superkingdom}', children=[
                                    dbc.Accordion(
                                        [
                                            dbc.AccordionItem(title=f'Phylum: {term_phylum}', children=[
                                                dbc.Accordion(
                                                    [
                                                        dbc.AccordionItem(title=f'Class: {term_class}', children=[
                                                            dbc.Accordion(
                                                                [
                                                                    dbc.AccordionItem(title=f'Order: {term_order}', children=[
                                                                        dbc.Accordion(
                                                                            [
                                                                                dbc.AccordionItem(title=f'Family: {term_family}', children=[
                                                                                    dbc.Accordion(
                                                                                        [
                                                                                            dbc.AccordionItem(title=f'Genus: {term_genus}', children=[
                                                                                                dbc.Accordion(
                                                                                                    [
                                                                                                        dbc.AccordionItem(title=f'Species: {term_species}', children=[
                                                                                                            dbc.Accordion(
                                                                                                                [
                                                                                                                    dbc.AccordionItem(title=f'Subspecies: {term_subspecies}')
                                                                                                                ],
                                                                                                                flush=True,
                                                                                                            )
                                                                                                        ])
                                                                                                    ],
                                                                                                    flush=True,
                                                                                                )
                                                                                            ])
                                                                                        ],
                                                                                        flush=True,
                                                                                    )
                                                                                ])
                                                                            ],
                                                                            flush=True,
                                                                        )
                                                                    ])
                                                                ],
                                                                flush=True,
                                                            )
                                                        ])
                                                    ],
                                                    flush=True,
                                                )
                                            ])
                                        ],
                                        flush=True,
                                    )
                                ])
                            ],
                            flush=True,
                        )
                    ]),
                    dbc.Col([
                        html.H5(f'Part of the NetFlax network: {part_of_netflax}'),
                        html.H5(f'Proteome size: {proteome_size}'),
                        html.H5(f'Number of TAs: {number_of_ta}'),
                    ]),
                ])
            ]
        )
    elif search_term.startswith('WP_'):
        antitoxin_color = 'darkgreen'
        toxin_color = 'darkred'
        for row in df_netflax.itertuples():
            if search_term == row.at_accession:
                search_a = row.at_accession
                search_t = row.t_accession
                search_at_dom = row.at_domain
                search_t_dom = row.t_domain
                proteome_size = row.proteome_size
                text_color = antitoxin_color
                chain_colors = {'E': antitoxin_color}
            elif search_term == row.t_accession:
                search_a = row.at_accession
                search_t = row.t_accession
                search_at_dom = row.at_domain
                search_t_dom = row.t_domain
                proteome_size = row.proteome_size
                text_color = toxin_color
                chain_colors = {'E': toxin_color}
            else:
                continue
        
        structure_data, styles = get_structural_data(search_term)

        return html.Div(
            children=[
                dbc.Row([
                    html.H4(f'Search results for "{search_term}"', style={'color': text_color})
                ]),
                dbc.Row([
                    dbc.Col([
                        html.H5(f'Antitoxin: {search_a}', style={'color': antitoxin_color}),
                        html.H5(f'Antitoxin Domain: {search_at_dom}', style={'color': antitoxin_color}),
                        html.Br(),
                        html.H5(f'Toxin: {search_t}', style={'color': toxin_color}),
                        html.H5(f'Toxin Domain: {search_t_dom}', style={'color': toxin_color}),
                        html.Br(),
                        html.H5(f'Proteome Size: {proteome_size}', style={'color': 'black'}),

                    ]),
                    dbc.Col([
                            dashbio.Molecule3dViewer(
                            id='dashbio-default-molecule3d',
                            modelData=structure_data,
                            styles=styles,
                        )
                    ]),
                    dbc.Col([
                        "Selection data",
                        html.Hr(),
                        html.Div(id='molecule-info-container')
                    ])
                ]),
            ]
        )   
    elif search_term.startswith('D') or search_term.startswith('M'):
        # Fetch the nodes from the DataFrame
        nodes_at = df_netflax.loc[df_netflax['at_domain'] == search_term, 't_domain'].tolist()
        nodes_t = df_netflax.loc[df_netflax['t_domain'] == search_term, 'at_domain'].tolist()

        # Combine the nodes from both columns
        nodes = nodes_at + nodes_t

        # Define the edges for the given node
        edges = [{'data': {'source': search_term, 'target': node}} for node in nodes if node != search_term]
        # Define the layout
        layout = {'name': 'grid'}
        # Combine nodes, edges, and layout into the elements list
        elements = [{'data': {'id': node, 'label': node}} for node in nodes] + edges

        return html.Div(
            children=[
                dbc.Row([
                    html.H4(f'Search results for "{search_term}"'),
                ]),
                dbc.Row([
                    cyto.Cytoscape(
                    id='cyto-network',
                    elements=elements,
                    layout=layout,
                    style={'width': '100%', 'height': '400px'}
                    )
                ]),
            ])
    else:
        print(f'{search_term} not specified')




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

