# INTERACTIVITY CODE

# Import packages
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

# Import data
from data.data_prep import *

# Import functions
from functions.a1_protein_coords import *
from functions.a2_protein_strucuture import *
from functions.a3_create_logos import *

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
            [df['superkingdom'], 
            df['phylum'], 
            df['class'], 
            df['order'], 
            df['family'], 
            df['genus'], 
            df['taxa']]).tolist()))
    elif button_id == 'accession-number':
        # Make a list of all ac
        options = list(set(pd.concat([df['at_accession'], df['t_accession']]).tolist()))
    elif button_id == 'node':
        # Make a list of all nodes
        options = list(set(pd.concat([df['at_domain'], df['t_domain']]).tolist()))
    else:
        # Otherwise the dropdown menu is empty
        options = []
    
    return [{'label': option, 'value': option} for option in options]




# 1. SLIDER FOR TAXONOMIC LEVEL

# Create a list of paths with different number of levels
paths = {
    0: ['superkingdom'],
    1: ['superkingdom', 'phylum'],
    2: ['superkingdom', 'phylum', 'class'],
    3: ['superkingdom', 'phylum', 'class', 'order'],
    4: ['superkingdom', 'phylum', 'class', 'order', 'family'],
    5: ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus'],
    6: ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'taxa']
}

@callback(
    Output('a1_taxonomy_sunburst', 'figure'),
    Output('results-container', 'children'),
    Input('taxonomy_level_slider', 'value'),
    Input('search-dropdown', 'value')
)
def update_sunburst_level(level=None, search_term=None):
    '''
    A callback to update the taxonomy wheel figure through:
        1. Search by taxonomy, accession, or node
        2. The slider (taxonomy level)
    Default level is set at 'order' (3). 

    Args:
        level: The taxonomic level
        search_term: The protein accession number
    
    Returns:
        Returns an updated wheel figure based on the search input and
        the taxonomic level. It also updates the results output box on
        the right-hand side. This is unique for each category.
    '''

    # ------------------------------ SEARCH ----------------------------    
    if search_term != None:
        # 1. Search by accession
        if search_term.startswith('WP_'):
            df = df_netflax.copy()
            # Filter the dataframe for the selected search term
            mask = (df['at_accession'].str.contains(search_term, case=False)) | (df['t_accession'].str.contains(search_term, case=False))
            filtered_df = df.loc[mask]

            # Get the last ring based on the taxa of the selected row
            last_ring = ""
            if len(filtered_df[filtered_df['at_accession'] == search_term]['taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['at_accession'] == search_term]['taxa'].values[0]
            elif len(filtered_df[filtered_df['t_accession'] == search_term]['taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['t_accession'] == search_term]['taxa'].values[0]

            # Set the color of the matching segment
            df['color'] = wedge_non_highlight
            df.loc[df['taxa'] == last_ring, 'color'] = wedge_highlight

            # Create the sunburst for the whole dataset
            fig = px.sunburst(
                data_frame=df,
                path=paths[6],
                color='color',
                color_discrete_map={
                    'grey': wedge_non_highlight, 
                    'blue': wedge_highlight
                },
                branchvalues='total'
            )

            fig.update_traces(
                marker=dict(line=dict(color=page_background, width=0.5)),
                hovertemplate='<b>%{label} </b> <br>Taxonomy: %{id}<br>Number of TAs: %{value}',
            )
            fig.update_layout(
                plot_bgcolor=transparent_background,
                paper_bgcolor=transparent_background
            )
            
            # Prepare output
            sunburst_fig = fig
            dataset = df_netflax[df_netflax.values == search_term]

            # Get protein logos
            fig_antitoxin, fig_toxin = create_protein_logos(search_term)
            
            # Get structure for protein
            structure_data, styles, chain_sequence = visualising_protein(search_term)

            return sunburst_fig, html.Div(
                children=[
                    dbc.Row([
                        html.H4(f'Search results for "{search_term}"'),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(
                                    id='antitoxin-logo', 
                                    figure=fig_antitoxin, 
                                    )
                            ], width=5),
                            dbc.Col(width=1),
                            dbc.Col([
                                dcc.Graph(
                                    id='toxin-logo', 
                                    figure=fig_toxin)
                            ], width=5)
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dashbio.Molecule3dViewer(
                                    id='dashbio-default-molecule3d',
                                    modelData=structure_data,
                                    styles=styles
                                )
                            ]),
                            dbc.Col([
                                dashbio.SequenceViewer(
                                    id='dashbio-default-sequenceviewer',
                                    sequence=chain_sequence,
                                    #title=f'Protein Sequence ({antitoxin}/{toxin})'
                                )
                            ])
                        ])
                    ])
                ]
            )  

        # 2. Search by node      
        elif search_term.startswith('D') or search_term.startswith('M') or search_term.startswith('Panacea'):
            # Filter the dataframe for the selected search term
            df = df_netflax.copy()
            mask = (df['at_domain'].str.contains(search_term, case=False)) | (df['t_domain'].str.contains(search_term, case=False))
            filtered_df = df.loc[mask]

            # Get the last ring based on the taxa of the selected row
            last_ring = ""
            if len(filtered_df[filtered_df['at_domain'] == search_term]['taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['at_domain'] == search_term]['taxa'].values[0]
            elif len(filtered_df[filtered_df['t_domain'] == search_term]['taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['t_domain'] == search_term]['taxa'].values[0]

            # Set the color of all matching segments to lightblue
            df['color'] = wedge_non_highlight
            df.loc[df['taxa'] == last_ring, 'color'] = wedge_highlight

            # Create the sunburst for the whole dataset
            fig = px.sunburst(
                data_frame=df,
                path=paths[6],
                color='color',
                color_discrete_map={
                    'grey': wedge_non_highlight, 
                    'blue': wedge_highlight
                },
                branchvalues='total'
            )

            fig.update_traces(
                marker=dict(line=dict(color=page_background, width=0.5)),
                hovertemplate='<b>%{label} </b> <br>Taxonomy: %{id}<br>Number of TAs: %{value}',
            )
            fig.update_layout(
                plot_bgcolor=transparent_background,
                paper_bgcolor=transparent_background
            )

            sunburst_fig = fig
            # Filter netflax_df by the search term
            dataset = df_netflax[df_netflax.values == search_term]
            
            return sunburst_fig, html.Div(
            children=[
                dbc.Row([
                    html.H4(f'Search results for "{search_term}"'),
                    dbc.Row([
                        'InfoBox'
                    ]),
                    dbc.Row([
                        dbc.Col([

                        ]),
                        dbc.Col([

                        ])
                    ]),
                    dbc.Row([
                        "Selection data",
                        html.Hr(),
                        html.Div(id = 'molecule-info-container')
                    ]),
                    dbc.Row([
                        'Filtered NetFlax Table Results',
                        dash_table.DataTable(
                            id = 'table',
                            data = dataset.to_dict('records'),
                            fixed_rows = {'headers': True},
                            style_cell = {'minWidth': 95, 'maxWidth': 95, 'width': 95})
                    ]),
                ]),
            ]
        )    
 


        # 3. Search by taxonomy at any level
        else:
            df = df_netflax.copy()
             # Set the color of the matching segment to red
            df['color'] = wedge_non_highlight

            # Determine in which column the search term is present
            if search_term in df['superkingdom'].values:
                level = 0
                df.loc[df['superkingdom'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['phylum'].values:
                level = 1
                df.loc[df['phylum'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['class'].values:
                level = 2
                df.loc[df['class'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['order'].values:
                level = 3
                df.loc[df['order'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['family'].values:
                level = 4
                df.loc[df['family'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['genus'].values:
                level = 5
                df.loc[df['genus'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['taxa'].values:
                level = 6
                df.loc[df['taxa'] == search_term, 'color'] = wedge_highlight
            else:
                print(f'{search_term} does not exist')

            # Create the sunburst for the filtered dataset
            fig = px.sunburst(
                data_frame=df,
                path=paths[6],
                color='color',
                color_discrete_map={
                    'grey': wedge_non_highlight, 
                    'blue': wedge_highlight
                },
                branchvalues='total'
            )

            fig.update_traces(
                marker=dict(line=dict(color=page_background, width=0.5)),
                hovertemplate='<b>%{label} </b> <br>Taxonomy: %{id}<br>Number of TAs: %{value}',
            )
            fig.update_layout(
                plot_bgcolor=transparent_background,
                paper_bgcolor=transparent_background
            )

            sunburst_fig = fig
            # Filter netflax_df by the search term
            dataset = df_netflax[df_netflax.values == search_term]
            
            return sunburst_fig, html.Div(
            children=[
                dbc.Row([
                    html.H4(f'Search results for "{search_term}"'),
                    dbc.Row([
                        'InfoBox'
                    ]),
                    dbc.Row([
                        dbc.Col([

                        ]),
                        dbc.Col([

                        ])
                    ]),
                    dbc.Row([
                        "Selection data",
                        html.Hr(),
                        html.Div(id = 'molecule-info-container')
                    ]),
                    dbc.Row([
                        'Filtered NetFlax Table Results',
                        dash_table.DataTable(
                            id = 'table',
                            data = dataset.to_dict('records'),
                            fixed_rows = {'headers': True},
                            style_cell = {'minWidth': 95, 'maxWidth': 95, 'width': 95})
                    ]),
                ]),
            ]
        )    
 

    # ------------------------------ SLIDER ----------------------------

    # Create a sunburst chart with the selected number of levels
    dataset = df_netflax
    if level is None:
        level = 3  # default value if level is not selected

    # Creating the plot    
    fig = sunburst_plot = px.sunburst(
        data_frame = dataset,
        path = paths[level],
        color = 'superkingdom',
        color_discrete_sequence = px.colors.qualitative.Pastel,
    )
    fig.update_traces(
        marker = dict(line = dict(color = page_background, width = 0.75)),
        hovertemplate='<b>%{label} </b> <br>Taxonomy: %{id}<br>Number of TAs: %{value}',
    )
    fig.update_layout(
        plot_bgcolor = transparent_background,
        paper_bgcolor = transparent_background)
    
    sunburst_fig = fig

    return sunburst_fig, html.Div(
            children=[
                dbc.Row([
                    html.H4(f'Search results for "{search_term}"'),
                    dbc.Row([
                        'InfoBox'
                    ]),
                    dbc.Row([
                        dbc.Col([

                        ]),
                        dbc.Col([

                        ])
                    ]),
                    dbc.Row([
                        "Selection data",
                        html.Hr(),
                        html.Div(id = 'molecule-info-container')
                    ]),
                    dbc.Row([
                        'Filtered NetFlax Table Results',
                        dash_table.DataTable(
                            id = 'table',
                            data = dataset.to_dict('records'),
                            fixed_rows = {'headers': True},
                            style_cell = {'minWidth': 95, 'maxWidth': 95, 'width': 95})
                    ]),
                ]),
            ]
        )    
 



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
    Output('error-message', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def check_error_message(n_intervals):
    # Assuming `get_error_message()` is a function that returns the error message
    error_message = get_error_message()
    
    if error_message:
        return html.Div(error_message, className='error-text')
    else:
        return ''