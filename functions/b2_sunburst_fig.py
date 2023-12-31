# FUNCTIONS FOR CREATING SUNBURST FIGURE AND RESULTS

# Import packages
import pandas as pd
import plotly.express as px


# Import data
from data.data_prep import *

# Import aesthetetics
from assets.color_scheme import *



# Create a list of paths with different number of levels
paths = {
    0: ['Superkingdom'],
    1: ['Superkingdom', 'Phylum'],
    2: ['Superkingdom', 'Phylum', 'Class'],
    3: ['Superkingdom', 'Phylum', 'Class', 'Order'],
    4: ['Superkingdom', 'Phylum', 'Class', 'Order', 'Family'],
    5: ['Superkingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus'],
    6: ['Superkingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Taxa']
}


def create_sunburst_figure(df, level=None, color_column=None, default='yes'):
    '''
    Creates a sunburst figure based on the provided dataframe, color column, and highlight value.

    Args:
        df: The dataframe containing the data for the sunburst figure.
        color_column: The column in the dataframe to use for coloring the segments.
        highlight_value: The value in the color column to highlight.

    Returns:
        Returns the created sunburst figure.
    '''
    if default == 'yes':
        fig = px.sunburst(
            data_frame=df,
            path=paths[level],
            color='Superkingdom',
            color_discrete_map={
                'purple': wheel_bacteria,
                'yellow': wheel_archea,
                'pink': wheel_virus
            },
            color_discrete_sequence=[wheel_bacteria, wheel_archea, wheel_virus]
        )
    else:
        fig = px.sunburst(
            data_frame=df,
            path=paths[level],
            color=color_column,
            color_discrete_map={
                wedge_non_highlight : wedge_non_highlight, 
                wedge_highlight : wedge_highlight
            },
            branchvalues='total', 
        )

    fig.update_traces(
        marker=dict(line=dict(color=page_background, width=0.5)),
        hovertemplate='<b>%{label} </b> <br>Taxonomy: %{id}<br>Number of TAs: %{value}',
    )
    fig.update_layout(
        plot_bgcolor=transparent_background,
        paper_bgcolor=transparent_background
    )

    return fig


