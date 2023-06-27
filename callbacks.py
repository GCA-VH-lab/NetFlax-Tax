# INTERACTIVITY CODE

# Import packages
import pandas as pd
import re
import dash
import requests
import numpy as np

import plotly.express as px
from dash import html, dcc, callback, ctx, dash_table
from dash.dependencies import Input, Output, State, ALL


import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_cytoscape as cyto

# Import data
from data.data_prep import *

# Import functions
from functions.a1_protein_coords import *
from functions.a2_protein_strucuture import *
from functions.a3_create_logos import *
from functions.b1_table import *
from functions.b2_sunburst_fig import *

# Import aesthetetics
from assets.color_scheme import *



# ---------------------------- CALLBACKS -------------------------------

# 0. Updating dropdown list based on button
@callback(
    Output('search-dropdown', 'options'), 
    [
        Input('taxonomy', 'n_clicks'),
        Input('accession-number', 'n_clicks'),
        Input('node', 'n_clicks')
    ],
)

def update_dropdown_options(taxa_click=None, acc_click=None, node_click=None):
    '''
    A callback to update the dropdown menu based on the selected
    category.

    Args:
        taxa_click: Clicking the Taxonomy button
        acc_click: Clicking the Accession number button
        node_click: Clicking the Node button
    
    Returns:
        Populates the dropdown menu with a list of all TAs based on one
        of the 3 categories mentioned above.
    '''
    # The dataset used
    df = df_netflax

    # 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'taxonomy':
        # Make a list with all values of all the taxonomy columns
        options = list(set(pd.concat(
            [df['Superkingdom'], 
            df['Phylum'], 
            df['Class'], 
            df['Order'], 
            df['Family'], 
            df['Genus'], 
            df['Taxa']]).tolist()))
        options = sorted(options)
    elif button_id == 'accession-number':
        # Make a list of all ac
        options = list(set(pd.concat([df['AT Accession'], df['T Accession']]).tolist()))
        options = sorted(options)
    elif button_id == 'node':
        # Make a list of all nodes
        options = list(set(pd.concat([df['AT Domain'], df['T Domain']]).tolist()))
        options = sorted(options)
    else:
        # Otherwise the dropdown menu is empty
        options = []
    
    return [{'label': option, 'value': option} for option in options]




# 1. SLIDER FOR TAXONOMIC LEVEL

@callback(
    Output('a1_taxonomy_sunburst', 'figure'),
    Output('table-container', 'children'),
    Input('taxonomy_level_slider', 'value'),
    Input('search-dropdown', 'value'),
    Input({"type": "ta-button", "index": ALL}, "n_clicks"),
    State({"type": "ta-button", "index": ALL}, "id")
)
def update_sunburst_level(level=None, search_term=None, button_clicks=None, button_ids=None):
    '''
    A callback to update the taxonomy wheel figure through:
        1. Search by taxonomy, accession, or node
        2. The slider (taxonomy level)
    Default level is set at 'Order' (3). 

    Args:
        level: The taxonomic level
        search_term: The protein accession number
        button_index: 

    Returns:
        Returns an updated wheel figure based on the search input and
        the taxonomic level. It also updates the results output box on
        the right-hand side. This is unique for each category.
    '''
    # -------------------------- VIEW STRUCTURE ------------------------    
    if button_clicks:
        for clicks, button_id in zip(button_clicks, button_ids):
            if clicks and button_id:
                button_name = button_id.get('index')
                search_term = button_name.split('(')[0]
                break

    # ------------------------------ SEARCH ----------------------------    
    if search_term != None:
        # 1. Search by accession
        if search_term.startswith('WP_'):
            df = df_netflax.copy()
            # Filter the dataframe for the selected search term
            mask = (df['AT Accession'].str.contains(search_term, case=False)) | (df['T Accession'].str.contains(search_term, case=False))
            filtered_df = df.loc[mask]

            # Get the last ring based on the taxa of the selected row
            last_ring = ""
            if len(filtered_df[filtered_df['AT Accession'] == search_term]['Taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['AT Accession'] == search_term]['Taxa'].values[0]
            elif len(filtered_df[filtered_df['T Accession'] == search_term]['Taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['T Accession'] == search_term]['Taxa'].values[0]

            # Set the color based on matching or non-matching segments
            df['color'] = wedge_non_highlight
            df.loc[df['Taxa'] == last_ring, 'color'] = wedge_highlight

            # Updated dataset          
            dataset = df_netflax[df_netflax.values == search_term]
            level = 6

            # Get protein logos
            fig_antitoxin, fig_toxin = create_protein_logos(search_term)
            
            # Get structure for protein
            structure_data, styles, chain_sequence = visualising_protein(search_term)

            # Get sunburst fig
            sunburst_fig = create_sunburst_figure(df, level, 'color', default='no')

            results_div = html.Div([
                html.Div([
                    html.Br(style={'padding':'10px'}),
                    dbc.Container([
                        dbc.Row(
                            html.H6(
                                f'Search results for "{search_term}"',
                                style={
                                    'margin-top': '40px',
                                    'padding': '20px',
                                    'background-color': accent_medium,
                                    'border-radius': '10px',
                                },
                            )
                        ),
                        dbc.Row([
                            dbc.Col([
                                html.H6('Antitoxin'),
                                dcc.Graph(
                                    id='antitoxin-logo', 
                                    figure=fig_antitoxin,
                                    config={
                                        'displayModeBar': False
                                    }
                                ),
                            ],  width={'size': 5}),
                            dbc.Col(width={'size': 1}), 
                            dbc.Col([
                                html.H6('Toxin'),
                                dcc.Graph(
                                    id='toxin-logo', 
                                    figure=fig_toxin,
                                    config={
                                        'displayModeBar': False
                                    }
                                ),
                            ],  width={'size': 5}),
                        ]),
                        dbc.Row(
                            html.H6('Antitoxin-Toxin Structure')   
                            ),
                        dbc.Row([
                            dbc.Col([
                                dashbio.Molecule3dViewer(
                                    id='dashbio-default-molecule3d',
                                    modelData=structure_data,
                                    styles=styles
                                ),
                            ],  width={'size': 10}, 
                                style={'padding':'10px'})
                        ]),
                    ],  style={
                            'background-color': page_background,
                            'border-radius': '10px',
                            'width': '100%', 
                            'margin': '0 auto', 
                        })
                ])
            ], style={'max-height': '90vh'})


            return sunburst_fig, results_div  

        # 2. Search by node      
        elif search_term.startswith('D') or search_term.startswith('M') or search_term.startswith('Panacea'):
            # Filter the dataframe for the selected search term
            df = df_netflax.copy()
            mask = (df['AT Domain'].str.contains(search_term, case=False)) | (df['T Domain'].str.contains(search_term, case=False))
            filtered_df = df.loc[mask]

            # Get the last ring based on the taxa of the selected row
            last_ring = ""
            if len(filtered_df[filtered_df['AT Domain'] == search_term]['Taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['AT Domain'] == search_term]['Taxa'].values[0]
            elif len(filtered_df[filtered_df['T Domain'] == search_term]['Taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['T Domain'] == search_term]['Taxa'].values[0]

            # Set the color based on matching or non-matching segments
            df['color'] = np.where(df['Taxa'].isin(filtered_df['Taxa']), wedge_highlight, wedge_non_highlight)

            # New dataset
            level = 6
            dataset = df[df.values == search_term]

            # Creating results
            sunburst_fig = create_sunburst_figure(df, level, 'color', default='no')
            table_title = f'Dataset filtered based on node: {search_term}'
            table = create_table(dataset)
            results_div = create_results_div(table_title, table, dataset)

            return sunburst_fig, results_div  
 
        # 3. Search by taxonomy at any level
        else:
            df = df_netflax.copy()
             # Set the color of the matching segment to red
            df['color'] = wedge_non_highlight

            # Determine in which column the search term is present
            if search_term in df['Superkingdom'].values:
                level = 0
                df.loc[df['Superkingdom'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['Phylum'].values:
                level = 1
                df.loc[df['Phylum'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['Class'].values:
                level = 2
                df.loc[df['Class'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['Order'].values:
                level = 3
                df.loc[df['Order'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['Family'].values:
                level = 4
                df.loc[df['Family'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['Genus'].values:
                level = 5
                df.loc[df['Genus'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['Taxa'].values:
                level = 6
                df.loc[df['Taxa'] == search_term, 'color'] = wedge_highlight
            else:
                print(f'{search_term} does not exist')

            # New dataset
            level = 6
            dataset = df[df.values == search_term]

            # Creating results
            sunburst_fig = create_sunburst_figure(df, level, 'color', default='no')
            table_title = f'Dataset filtered based on {search_term}'
            table = create_table(dataset)
            results_div = create_results_div(table_title, table, dataset)

            return sunburst_fig, results_div  

    # ----------------------------- DEFAULT ----------------------------

    # Create a sunburst chart with the selected number of levels
    if level is None:
        level = 3  # default value if level is not selected

    # New dataset
    dataset = df_netflax

    # Creating results
    sunburst_fig = create_sunburst_figure(dataset, level)
    table_title = f'Complete NetFlax Dataset'
    table = create_table(dataset)
    results_div = create_results_div(table_title, table, dataset)

    return sunburst_fig, results_div  





# Update callback for Molecule3dViewer
@callback(
    Output('molecule-info-container', 'children'),
    Input('dashbio-default-molecule3d', 'selectedAtomIds')
)
def display_molecule_info(click_info):
    if click_info is None:
        return html.Div()  # Return empty div if no click info available
    else:
        atom_id = click_info['atom']
        chain_id = click_info['chain']
        element = click_info['elem']
        residue_name = click_info['residue_name']

        return html.Div([
            html.Div(f'Element: {element}'),
            html.Div(f'Chain: {chain_id}'),
            html.Div(f'Residue name: {residue_name}'),
            html.Br()
        ])



@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    df = create_results_div[2]
    return dcc.send_data_frame(df.to_csv, "mydf.csv", index=False)


