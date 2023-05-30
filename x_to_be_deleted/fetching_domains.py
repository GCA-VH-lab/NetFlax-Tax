import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import colorsys
import random
from itertools import islice
from functions.protein_logos.protein_coords import *


# # DATASET
# domain_file = pd.read_csv('./netflax_domain_search.csv', sep = '\t', header = None)
# annot_file = pd.read_csv('./cdd_id_all_lut.txt', sep = '\t')


# 1. Merging the two traces into one plot
fig = make_subplots(shared_yaxes = True, shared_xaxes = True)                                                                               
                                                                                                    
# y_axes = df[0].nunique()*200
# x_axes = y_axes*3

y_axes = 900
x_axes = 3200

# 3. All lists
arrowList = []
domainList = []
xList_gene = []
yList_gene = []
xList_domain = []
yList_domain = []
y_tick_marks = []
labels = []
genes = []


for i in domain_file.iloc[:, 3]:
    if i != '':
        domain_file.iloc[:, 3] = domain_file.iloc[:, 3].str.replace("PF", "pfam")

for e, row2 in annot_file.iterrows():
    domain_code_2 = annot_file.iloc[:, 0][e]
    domain_name = annot_file.iloc[:, 1][e]
    for i in domain_file.iloc[:, 3]:
        domain_code_1 = i.split('.')[0]
        if domain_code_1 == domain_code_2:
            domain_file.iloc[:, 3] = domain_file.iloc[:, 3].replace(i, domain_name)

domain_dict = {
        'database': [],
        'domain_accession':[],
        'domain_code': [],
        'domain_start': [],
        'domain_end': [],
        'e_value': [],
        'score': [],
    }

domain_dict["database"] = list(domain_file.iloc[:, 1])
domain_dict["domain_accession"] = list(domain_file.iloc[:, 0])

for str in domain_file.iloc[:, 10]:
    if str != '':
        str1 = str.split('-')[0]
        domain_dict["domain_start"].append(str1)
        str2 = str.split('-')[1]
        domain_dict["domain_end"].append(str2)

domain_dict["domain_name"] = list(domain_file.iloc[:, 3])


# 4. Data file input
main_file = open('selected_operon_230122.tsv','r').read()
eg1 = main_file.split("\n\n\n\n")
y_level_m = 0
for m in eg1:
    if m != '':
        row1 = 0
        entries1 = m.splitlines()
        ndoms=len(entries1)
        y_level_m = y_level_m - 20
        for entry in entries1: 
            items1 = entry.split("\t")
            gene_start = int(items1[5])
            gene_end = int(items1[6])
            gene_length = int(items1[1])
            gene_direction = items1[3]
            dom1_name = int(items1[4])
            id1 = items1[9][:14]                  

            # 4a. When genes are to small the arrow shape is distorted because the coordinates are too close to each other.
            #     This makes these genes longer to keep the shape of the arrow. 
            if gene_length < 100:
                gene_start = int(items1[5])-50
                gene_end = int(items1[6])+50
            else:
                gene_start = int(items1[5])
                gene_end = int(items1[6])


            #Colours (imported from FlaGs script)
            center=int(dom1_name)+1
            noProt=int(dom1_name)+2
            noProtP=int(dom1_name)+3
            noColor=int(dom1_name)+4
            
            color[noColor]='#ffffff'
            color[center]='#000000'
            color[noProt]='#f2f2f2'
            color[noProtP]='#f2f2f3'


            if dom1_name == 0:
                colorDict[dom1_name]='#ffffff'
            elif gene_start == 1:                    
                colorDict[dom1_name]='#000000'
            elif 'pseudogene_' in id1:
                colorDict[dom1_name]='#f2f2f2'
            elif 'tRNA_' in id1:
                colorDict[dom1_name]='#f2f2f3'
            else:
                if dom1_name not in colorDict:
                    colorDict[dom1_name] = '#d9d9d9'


            # 4b. Editing the label for each gene in the legend
            protein = (id1 + ' ' + '(' + ('Start: {}\tEnd: {}'.format(gene_start, gene_end)) + ')')
            #hover_text = 'ID: ' + id1 +'<br>Start: ' + str(gene_start) + '<br>End: ' + str(gene_end)

            arrow_head = 30
            arrow_width = 3 
            top_domain = 3
            top_domain_opacity = 0.7
            middle_domain = 2
            middle_domain_opacity = 0.7
            bottom_domain = 2
            bottom_domain_opacity = 0.5

            # 4c. Drawing the genes as polygons/arrows
            if gene_direction == '-':
                xList_gene = [gene_start+arrow_head, gene_start, gene_start+arrow_head, gene_end, gene_end, gene_start+arrow_head]
                yList_gene = [y_level_m-arrow_width, y_level_m, y_level_m+arrow_width, y_level_m+arrow_width, y_level_m-arrow_width, y_level_m-arrow_width]
                arrowList.append(fig.add_trace(go.Scatter(x = xList_gene, y = yList_gene, fill="toself", fillcolor='#d9d9d9', opacity = 0.5, line=(dict(color = '#bfbfc0')), mode = 'lines+text')))
            elif gene_direction == '+':
                xList_gene = [gene_start, gene_start, gene_end-arrow_head, gene_end, gene_end-arrow_head, gene_start]
                yList_gene = [y_level_m-arrow_width, y_level_m+arrow_width, y_level_m+arrow_width, y_level_m, y_level_m-arrow_width, y_level_m-arrow_width] 
                arrowList.append(fig.add_trace(go.Scatter(x = xList_gene, y = yList_gene, fill="toself", fillcolor='#d9d9d9', opacity = 0.5, line=(dict(color = '#bfbfc0')), mode = 'lines+text')))
      

            # 5. Annotating each polygon/arrow with family number
            text_x = gene_start + (gene_length/2.2)
            if dom1_name != 0 and gene_start != 1 and 'pseudogene_' not in id1 and 'tRNA_' not in id1:
                fig.add_annotation(x = text_x, y = y_level_m, xref='x', yref='y', text = dom1_name, font = dict(color = "black", size = 10, family = "Open Sans"), showarrow = False)
            else:
                pass

  
            # 6. Domains file input
            for i, row in domain_file.iterrows(): 
                domain_start_original = int(domain_dict["domain_start"][i])*3
                domain_size = ((int(domain_dict["domain_end"][i])*3)-((int(domain_dict["domain_start"][i])*3)))
                domain_name = domain_dict["domain_name"][i]
                database = domain_dict["database"][i]
                id2 = domain_dict["domain_accession"][i]
                
                if domain_name in domain_color_dict['domain_names']:
                    domain_row = domain_color_file[domain_color_file['Domain name'] == domain_name].index[0]
                    #domain_color = domain_color_file['Color code'][domain_row]
                    domain_color = '#787777'
                else:
                    domain_color = '#787777'

                # 6a. Editing the label for each domain in the legend
                domain = ('     ' + database + ': ' + domain_name)


                # 1. PFAM domains
                if database == 'pfam':
                    y_level_d = y_level_m
                    if id2 == id1:
                        domain_start = gene_start + domain_start_original
                        domain_end = domain_start + domain_size
                        if gene_end-arrow_head < domain_end < gene_end and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, gene_end-arrow_head, (gene_end-arrow_head) + (gene_end-domain_end), (gene_end-arrow_head) + (gene_end-domain_end), gene_end-arrow_head, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d+top_domain/2,  y_level_d-top_domain/2, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain)))                                 
                        elif gene_start < domain_start < gene_start+arrow_head and gene_direction == '-':
                            xList_domain = [gene_start+arrow_head, (gene_start+arrow_head) - (domain_start-gene_start),  (gene_start+arrow_head) - (domain_start-gene_start), gene_start+arrow_head, domain_end, domain_end, gene_start+arrow_head]
                            yList_domain = [y_level_d-top_domain, y_level_d-top_domain/2, y_level_d+top_domain/2, y_level_d+top_domain,  y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain)))                       
                        elif domain_end <= gene_end and domain_start > gene_start+arrow_head and gene_direction == '-':           
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain)))
                        elif domain_start >= gene_start and gene_direction == '-':
                            xList_domain = [domain_start+arrow_head, domain_start, domain_start+arrow_head, domain_end, domain_end, domain_start+arrow_head]
                            yList_domain = [y_level_d-top_domain, y_level_d, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain)))
                        elif domain_start <= gene_start and domain_end < gene_end-arrow_head and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain)))
                        elif domain_start <= gene_start and domain_end <= gene_end and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, domain_end-arrow_head, domain_end, domain_end-arrow_head, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain)))
                        elif domain_end <= gene_end and domain_start >= gene_start:
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain)))
            
                        # 6c. Placing domain anontation above the domain.
                        text_x = domain_start + (domain_size/2)
                        fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)

                # 2. PDB domains
                if database == 'pdb':
                    if id2 == id1:
                        domain_start = gene_start + domain_start_original
                        domain_end = domain_start + domain_size
                        y_level_d = y_level_m
                        if gene_end-arrow_head < domain_end < gene_end and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, gene_end-arrow_head, (gene_end-arrow_head) + (gene_end-domain_end), (gene_end-arrow_head) + (gene_end-domain_end), gene_end-arrow_head, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d+top_domain/2,  y_level_d-top_domain/2, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines', name = domain)))                                 
                        elif gene_start < domain_start < gene_start+arrow_head and gene_direction == '-':
                            xList_domain = [gene_start+arrow_head, (gene_start+arrow_head) - (domain_start-gene_start),  (gene_start+arrow_head) - (domain_start-gene_start), gene_start+arrow_head, domain_end, domain_end, gene_start+arrow_head]
                            yList_domain = [y_level_d-top_domain, y_level_d-top_domain/2, y_level_d+top_domain/2, y_level_d+top_domain/2,  y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines', name = domain)))                       
                        elif domain_end <= gene_end and domain_start > gene_start+arrow_head and gene_direction == '-':           
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines', name = domain)))
                        elif domain_start >= gene_start and gene_direction == '-':
                            xList_domain = [domain_start+arrow_head, domain_start, domain_start+arrow_head, domain_end, domain_end, domain_start+arrow_head]
                            yList_domain = [y_level_d-top_domain, y_level_d, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines', name = domain)))
                        elif domain_start <= gene_start and domain_end < gene_end-arrow_head and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines', name = domain)))
                        elif domain_start <= gene_start and domain_end <= gene_end and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, domain_end-arrow_head, domain_end, domain_end-arrow_head, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines', name = domain)))
                        elif domain_end <= gene_end and domain_start >= gene_start:
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines', name = domain)))
            
                        # 6c. Placing domain anontation above the domain.
                        text_x = domain_start + (domain_size/2)
                        fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)


                # 2. CDD domains
                if database == 'cdd':
                    if id2 == id1:
                        y_level_d = y_level_m - 4
                        domain_start = gene_start + domain_start_original
                        domain_end = domain_start + domain_size
                        if gene_end-arrow_head < domain_end < gene_end and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, gene_end-arrow_head, (gene_end-arrow_head) + (gene_end-domain_end), (gene_end-arrow_head) + (gene_end-domain_end), gene_end-arrow_head, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d+top_domain/2,  y_level_d-top_domain/2, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines', name = domain)))                                 
                        elif gene_start < domain_start < gene_start+arrow_head and gene_direction == '-':
                            xList_domain = [gene_start+arrow_head, (gene_start+arrow_head) - (domain_start-gene_start),  (gene_start+arrow_head) - (domain_start-gene_start), gene_start+arrow_head, domain_end, domain_end, gene_start+arrow_head]
                            yList_domain = [y_level_d-top_domain, y_level_d-top_domain/2, y_level_d+top_domain/2, y_level_d+top_domain/2,  y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines', name = domain)))                       
                        elif domain_end <= gene_end and domain_start > gene_start+arrow_head and gene_direction == '-':           
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines', name = domain)))
                        elif domain_start >= gene_start and gene_direction == '-':
                            xList_domain = [domain_start+arrow_head, domain_start, domain_start+arrow_head, domain_end, domain_end, domain_start+arrow_head]
                            yList_domain = [y_level_d-top_domain, y_level_d, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines', name = domain)))
                        elif domain_start <= gene_start and domain_end < gene_end-arrow_head and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines', name = domain)))
                        elif domain_start <= gene_start and domain_end <= gene_end and gene_direction == '+':
                            xList_domain = [domain_start, domain_start, domain_end-arrow_head, domain_end, domain_end-arrow_head, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines', name = domain)))
                        elif domain_end <= gene_end and domain_start >= gene_start:
                            xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                            yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d-top_domain, y_level_d-top_domain]
                            domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines', name = domain)))
            
                        # 6c. Placing domain anontation above the domain.
                        text_x = domain_start + (domain_size/2)
                        fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)



            # 7. Setting the y labels i.e. the organism name and accession nr etc.
            y_tick_marks += [y_level_m]
            labels += [items1[0]]
            genes += [items1[9]]

            row1 = row1 + 1
            print(m)


# 8. Changing the download format of the .html as .svg instead of the defaul .png
config = {'toImageButtonOptions': {'format': 'svg','filename': 'FlaGs','scale': 1}}


# 9. Graph layout
fig.update_xaxes(visible = False)
fig.update_yaxes(visible = True, showgrid = False, showline = False, autorange = True, automargin = True, showticklabels = True, tickvals = y_tick_marks, ticktext = labels, ticklen = 20, tickmode = 'array', titlefont = dict(family = 'Open Sans', size = 8))
fig.update_layout(autosize=False, width=x_axes, height=y_axes, margin=dict(l=100,r=500,b=100,t=100,pad=100),paper_bgcolor='white', plot_bgcolor='white', showlegend = True)

fig.show(config=config)

fig.write_html("test_230122.html")