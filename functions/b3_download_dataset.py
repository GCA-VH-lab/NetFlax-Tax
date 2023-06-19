
# Import packages
import base64
import pandas as pd
from dash import html, dcc

# Import specifics
from assets.color_scheme import *


def create_downloadable_table(table):
    """
    Create a results div with a title, table, and download button.

    Args:
        title (str): Title of the results section.
        table (dash_html_components.Table): HTML table element.

    Returns:
        dash_html_components.Div: Results div with title, table, and download button.
    """
    # Create a unique ID for the download button
    download_id = 'download-button'

    # Convert the table to a CSV string
    csv_string = table_to_csv(table)

    # Create the download link
    download_link = html.A(
        'Download Dataset',
        id=download_id,
        download='dataset.csv',
        href='data:text/csv;base64,' + base64.b64encode(csv_string.encode()).decode(),
        target='_blank',
        style={
            'color': navigation_bar, 
            'text-decoration': 'none',
            'background-color': accent_light,
            'padding': '5px',
            'border-radius': '5px'
            },
    )

    return download_link



def table_to_csv(df):
    """
    Convert a pandas DataFrame to a CSV string.

    Args:
        df (pandas.DataFrame): DataFrame containing the table data.

    Returns:
        str: CSV string representation of the DataFrame.
    """
    # Select all rows and all columns except the last one
    df_without_last_column = df.iloc[:, :-1]

    # Convert the DataFrame to a CSV string
    csv_data = df_without_last_column.to_csv(index=False)

    return csv_data


