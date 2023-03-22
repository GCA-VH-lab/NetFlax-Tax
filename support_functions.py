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



def taxonomoy_barplot(df):
    data = pd.melt(
        df, 
        id_vars=['Row Labels'], 
        var_name='Category', 
        value_name='Value'
    )
    data['Percent'] = df['Percentage'] * 100
    color_map = {
        'Bacteria (NF)': bacteria_color_nf,
        'Bacteria (All)': bacteria_color,
        'Archaea (NF)': archaea_color_nf,
        'Archaea (All)': archaea_color,
        'Viruses (NF)': viruses_color_nf,
        'Viruses (All)': viruses_color,
    }
    barplot = px.bar(
        data, 
        y = 'Row Labels',
        x = 'Value',
        text = 'Percent',
        color = 'Category',
        color_discrete_map = color_map,
        barmode = 'stack',

    )
    barplot.update_traces(
        hovertemplate = 'f%<b>{y}: <br>Genome count: %{x}',
        showlegend = False
    )
    barplot.update_layout(
        title = 'Distribution of TAs',
        title_x = 0.5,
        font = dict(
            size = 12,
        ),
        height = len(data['Row Labels']) * 3,
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
            autorange = 'reversed',
            title_text = 'Phylum',
            titlefont = dict(size = 15),
            tickfont = dict(size = 10),
        ),
    )
    return barplot


def superkingdom_piechart(df_netflax):
    pie_chart = px.sunburst(
        data_frame = df_netflax,
        path = ['AT Domain', 'T Domain'], 
        maxdepth = -1
    )
    return pie_chart



def combinations_heatmap(df_netflax):
    pivot_1 = pd.pivot_table(
        df_netflax,
        values = ['Taxa'], 
        index = ['Phylum'],
        columns = ['AT : T Combination'],
        aggfunc = lambda x: len(x.unique())
    )

    data = pivot_1['Taxa']

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


