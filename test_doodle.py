import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
#import kaleido #required
import plotly.io as pio



# df_all = pd.read_excel('/Users/veda/Dropbox (Personal)/NetFlax/Stats_App/Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='2. All_Searched_Data')
# df_netflax = pd.read_excel('/Users/veda/Dropbox (Personal)/NetFlax/Stats_App/Dataset_S1_Updated.xlsx', engine='openpyxl', sheet_name='3. NetFlax_Data')
df_all = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')



def ta_distribution_table(level, df_nf, df_all, kingdom=None):
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
    
    # 4. Adding a percentage column to the new table
    table['percentage'] = ((table['taxa_x']/(table['taxa_x'] + table['taxa_y'])) * 100).round(2)
    table = table.sort_values('taxa_x', ascending=False)

    return table



def nf_or_not(row):
    if row['proteome_size'] > 0:
        return 'Yes'
    else:
        return 'No'

df_all['NetFlax'] = df_all.apply(lambda row: nf_or_not(row), axis = 1)

df = df_netflax.pivot_table(columns = ['at_t_combinations'], aggfunc = 'size')




print(df.to_string())

comb = df_netflax['at_t_combinations'].nunique()

# from scipy.stats import chi2_contingency

# for col in df_netflax.columns:
#     if df_netflax[col].dtype == object:
#         cross_tab = pd.crosstab(df_netflax["Phylum"], df_netflax[col])
#         chi2, p, dof, expected = chi2_contingency(cross_tab)
#         print(f"The p-value for association between column_A and {col} is {p}")



# Graph 1. Superkingdom overview
# fig = go.Figure(go.Sunburst(
#     values = [24466, 13551, 3286, 10449, 13, 466, 120],
#     labels = ['Total', 'Bacteria_All', 'Bacteria_NF', 'Viruses_All', 'Virsues_NF', 'Archaea_All', 'Archaea_NF' ],
#     parents = ['', 'Total', 'Bacteria_All', 'Total', 'Viruses_All', 'Total', 'Archaea_All'],
#     branchvalues = 'total'
# ))
# fig.show()

# Heat map
# pivot_1 = pd.pivot_table(
#     df_netflax,
#     values = ['Taxa'], 
#     index = ['Phylum'],
#     columns = ['Combination'],
#     aggfunc = lambda x: len(x.unique())
# )

# data = pivot_1['Taxa']

# fig = px.imshow(
#     data,
#     )
# fig.update_layout(
#     width = 2500, 
#     height = 1000,
#     yaxis_nticks=len(data),
#     xaxis_nticks=250,
#     # yaxis = dict(
#     #     range = [-1, len(data)]
#     # ),
#     # xaxis = dict(
#     #     range = [0, 250]
#     # ),
#     coloraxis_showscale = True,
#     margin=dict(t=10, b=10, l=10, r=10),
#     )  
# fig.show()

# pivot_nf = pd.pivot_table(
#     df_netflax,
#     values = ['Taxa'], 
#     index = ['Phylum'],
#     columns = ['Superkingdom'],
#     aggfunc = lambda x: len(x.unique())
# )
# pivot_all = pd.pivot_table(
#     df_all,
#     values = ['Taxa'], 
#     index = ['Phylum'],
#     columns = ['Superkingdom'],
#     aggfunc = lambda x: len(x.unique())
# )
# data = (pivot_nf.merge(pivot_all, on = 'Phylum'))


# for value in data:
#     for kingdom in data['Phylum']:
#         nf_value = ['Taxa_x']['Archaea'][value]
#         og_value = ['Taxa_y']['Archaea'][value]
#         data['Taxa_y']['Archaea'] == data['Taxa_y']['Archaea'].replace(value, og_value-nf_value)
    

# barplot = px.bar(
#     data, 
#     x = data['Superkingdom'], 
#     y = data['Phylum'],
#     color = 'Phylum'
# )
# barplot.update_yaxes(autorange = 'reversed')
# barplot.show()



# x and y given as DataFrame columns
# fig = px.scatter(
#     df_netflax, 
#     x=df_netflax['ATDomain'], 
#     y='Combination', 
#     color='Superkingdom',  
#     width=800, 
#     height=800)

# fig.update_layout(xaxis = {'dtick':1})
# fig.show()

fig = px.scatter(
    df, 
    x=df_netflax['ATDomain'], 
    y='Combination', 
    color='Superkingdom',  
    width=800, 
    height=800)

fig.update_layout(xaxis = {'dtick':1})
fig.show()

# Sunburst AT and T domains
# fig = px.sunburst(
#         data_frame = df_netflax,
#         path = ['TDomain', 'ATDomain'], 
#         maxdepth = -1
#     )
# config = {'toImageButtonOptions': {'format': 'svg','filename': 'FlaGs','scale': 1}}
# fig.show(config=config)

# pio.write_image(fig, 'plot.svg', format='svg')



# fig = px.bar_polar(
#     df_netflax,
#     r="Proteome size", 
#     theta="Combination", 
#     color="ATDomain",
#     color_discrete_sequence= px.colors.sequential.Plasma_r,
#     title="Part of a continuous color scale used as a discrete sequence"
# )
# fig.show()

# features = ['TDomain', 'ATDomain', 'Phylum']
# fig = px.scatter_matrix(
#     df_netflax,
#     dimensions=features, 
#     color = 'Superkingdom')

# fig.update_traces(diagonal_visible=False)
# fig.show()