import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

background_color = '#d2e0eb'
banner_color = '#c2cfda'

bacteria_color = '#B9B7EE'
archaea_color = '#FFBF86'
viruses_color = '#D488BB'

bacteria_color_nf = '#9494C2'
archaea_color_nf = '#D39E71'
viruses_color_nf = '#B0719D'

toxin_color = '#48B7B4'
antitoxin_color = '#D3E171'



def sunburst(df_all):
    color_discrete_sequence = ['', bacteria_color, bacteria_color, archaea_color, archaea_color, viruses_color, viruses_color]
    sunburst_plot = go.Figure(go.Sunburst(
        values = [24466, 13551, 3286, 10449, 13, 466, 120],
        labels = ['Total', 'Bacteria_All', 'Bacteria_NF', 'Viruses_All', 'Virsues_NF', 'Archaea_All', 'Archaea_NF' ],
        parents = ['', 'Total', 'Bacteria_All', 'Total', 'Viruses_All', 'Total', 'Archaea_All'],
        branchvalues = 'total',
        marker = dict(
            colors = color_discrete_sequence
        )
    ))
    sunburst_plot.update_layout(
        title = 'Superkingdom Overview',
        title_x = 0.5,
        font = dict(
            size = 12,
        ),
        margin = dict(l=10, r=10, t=30, b=10),
        paper_bgcolor = background_color
    )
    return sunburst_plot



def taxonomy_distribution_table(level, df_nf, df_all, kingdom=None):
    """
    Constructs a table from two pivots tables (different df).

    Parameters: 
    level (str): Taxonomy level at which to sort the table (possible: 
        'phylum', 'class', 'order', 'family', or 'genus')
    df_nf (df): Netflax dataset/sheet
    df_all (df): All searched genomes dataset/sheet
    kingdom (str): If specified, will only select genomes of given 
        kingdom (possible: 'Bacteria', 'Archaea', or 'Viruses')

    Returns:
    table (df): Table with three columns (1) netflax genome count, 
    (2) all searched genome count, and (3) the difference as percentage
    """
    
    # 1. Only keeping the TAs of the selected kingdom in the df
    if kingdom is not None:            
        df_all = df_all[df_all['superkingdom'] == kingdom]
        df_nf = df_nf[df_nf['superkingdom'] == kingdom]

    # 2. Creating pivot tables (isolating relevant columns)
    pivot_nf = df_nf.pivot_table(index=level, values='taxa', aggfunc='count')
    pivot_all = df_all.pivot_table(index=level, values='taxa', aggfunc='count')

    # 3. Merging the pivot tables
    table = pd.merge(pivot_nf, pivot_all, on=level)
    table = table.reset_index()
    
    # 4. Adding a percentage column to the new table
    table['percentage'] = ((table['taxa_x']/(table['taxa_x'] + table['taxa_y'])) * 100).round(2)
    table = table.sort_values('taxa_x', ascending=False)

    return table


def taxonomy_distribution_barplot(df, level):
    """
    Creates the taxonomy bar plot. 

    Parameters: 
    df (df): 
    level (str): Taxonomy level at which to sort the table (possible: 
        'phylum', 'class', 'order', 'family', or 'genus')

    Returns:
    barplot (plot): A barplot with number of TA pairs (x-axis) and
    level (y-axis)
    """
    barplot = px.bar(
        df, 
        x = ['taxa_x', 'taxa_y'],
        y = level,
        height = 120+25*len(df.index),
        text = 'percentage',
        color = level,
        barmode = 'stack',
    )
    barplot.update_traces(
        hovertemplate = 'f%<b>{y}: <br>Genome count: %{x}',
        showlegend = False, 
        textposition = ['none', 'outside']
    )
    barplot.update_layout(
        title = 'Distribution of TAs',
        title_x = 0.5,
        font = dict(
            size = 12,
        ),
        margin = dict(l=10, r=10, t=30, b=10, pad=10),
        paper_bgcolor = background_color,
        plot_bgcolor = background_color,
        bargap = 0.3,
        xaxis = dict(
            title_text = 'Number of Genomes',
            titlefont = dict(size = 15),
            tickfont = dict(size = 10)
        ),
        yaxis = dict(
            title_text = level,
            titlefont = dict(size = 15),
            tickfont = dict(size = 10),
        ),
    )
    return barplot


def superkingdom_piechart(df_netflax):
    pie_chart = px.sunburst(
        data_frame = df_netflax,
        path = ['at_domain', 't_domain'], 
        maxdepth = -1
    )
    return pie_chart



def combinations_heatmap(df_netflax):
    pivot_1 = pd.pivot_table(
        df_netflax,
        values = ['taxa'], 
        index = ['phylum'],
        columns = ['at_t_combinations'],
        aggfunc = lambda x: len(x.unique())
    )

    data = pivot_1['taxa']

    heatmap = px.imshow(
        data,
    )
    heatmap.update_layout(
        width = 2000, 
        height = 500,
        yaxis_nticks=len(data),
        xaxis_nticks=250,
        # yaxis = dict(
        #     range = [-1, len(data)]
        # ),
        # xaxis = dict(
        #     range = [0, 250]
        # ),
        coloraxis_showscale = True,
        margin=dict(t=10, b=10, l=10, r=10),
    )  
    return heatmap


