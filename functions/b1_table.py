# CREATING THE TABLE INCLUDING BUTTONS

# Import packages
import pandas
import dash
from dash import html
import dash_bootstrap_components as dbc

# Import data
from data.data_prep import *

# Import functions
from functions.b3_download_dataset import *

# Import specifics
from assets.color_scheme import *


def create_table(dataset):
    # List of TAs
    ta_list = dataset['ta_pair'].unique()

    # List for storing table rows
    table_rows = []

    # Iterate over the TAs and create a table row for each
    for ta in ta_list:
        button = dbc.Button(
            'View', 
            id={'type': 'ta-button', 'index': ta}, 
            className='mr-2',
            style={
                'height': '30px',
                'fontSize': '12px', 
                'verticalAlign': 'middle',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'backgroundColor': navigation_bar,
                'color': 'white'
            } 
        )
        table_row = html.Tr([
            html.Td(button),
            html.Td(ta),
            html.Td(dataset.loc[dataset['ta_pair'] == ta, 'taxa'].iloc[0]),
        ])
        table_rows.append(table_row)

    # Create the table
    table = html.Table([
        html.Thead([
            html.Tr([
                html.Th('Structure', style={'text-align': 'center'}),
                html.Th('TA Pair', style={'text-align': 'center'}),
                html.Th('Taxa', style={'text-align': 'center'}),
            ])
        ]),
        html.Tbody(table_rows)
    ], className='styled-table', style={'font-size': '12px'})

    return table




def create_results_div(title, table, dataset):
    '''
    Creates a results div with a title and table.

    Args:
        title: The title of the results div.
        table: The table to include in the results div.

    Returns:
        Returns the created results div.
    '''
    download_table = create_downloadable_table(dataset)

    return html.Div(
        children=[
            dbc.Container(
                children=[
                    dbc.Row(
                        html.H6(title),
                        style={
                            'margin-top': '40px',
                            'padding': '20px',
                            'background-color': accent_medium,
                            'border-radius': '10px',
                        },
                    ),
                    dbc.Row(
                        html.Div(
                            [
                                table,
                                html.Br(),
                            ],
                            className='table-container',
                            style={
                                'overflowX': 'auto',
                                'overflowY': 'scroll',
                                'maxHeight': '400px',
                                'margin-top': '30px',
                                'padding': '20px',
                                'max-width': '800px',
                            },
                        )
                    ),
                    html.Hr(style={'padding': '10px'}),
                    dbc.Row(
                        download_table,
                        style={
                            'padding': '10px',
                        },
                    ),
                ],
                style={
                    'background-color': page_background,
                    'border-radius': '10px',
                    'width': '100%', 
                    'margin': '0 auto', 
                },
            )
        ]
    )

