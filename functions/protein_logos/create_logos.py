import pandas as pd
import requests
import dash
from urllib.request import urlopen
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide
from functions.protein_logos.protein_coords import *
import plotly.graph_objs as go
from plotly.subplots import make_subplots



# DATASETS
df_all = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')
df_domains_original = pd.read_csv('./data/domains.txt', sep = '\t', header = 0)

# Filtering out the pdb rows of the domains file
df_domains = df_domains_original[~df_domains_original['database'].str.contains('pdb')]   # NOTE! pdb domain searches are ignored


def find_domains(antitoxin, toxin, dataset, accession_row):
    '''
    Find the domains of the specified antitoxin and toxin proteins.

    Args:
        antitoxin: Accession number of the antitoxin to be searched for
        toxin: Accession number of the toxin to be searched for
        dataset: The domain search file
        accession_row: Name of the column containing the accession numbers.

    Returns:
        A subset of the domain search file containing the domains 
        associated with the specified antitoxin and toxin proteins.
    '''
    # Filtering only for the domains in the toxin and antitoxin
    mask = dataset[accession_row].isin([antitoxin, toxin])

    # Filter the dataframe using the mask
    filtered_df = dataset[mask]

    # Checking if the antitoxin or toxin is missing
    if antitoxin not in filtered_df[accession_row]:
        print(f'The antitoxin: {antitoxin} is missing domains')
    elif toxin not in filtered_df[accession_row]:
        print(f'The toxin: {antitoxin} is missing domains')
    
    return filtered_df




def count_residues(pdb_file, chain_id):
    '''
    Counts the number of residues in a specified chain.

    Args:
        structure_data: a dictionary of the structure data from a PDB file
        chain_id: the chain ID of the chain to count residues for (A or B)

    Returns:
        The number of residues in the specified chain.
    '''

    # Create a list of residue IDs for the specified chain
    residues = []
    for atom in pdb_file['atoms']:
        if atom['chain'] == chain_id:
            residue_id = (atom['residue_name'], atom['residue_index'])
            if residue_id not in residues:
                residues.append(residue_id)

    # Return the number of unique residues in the list
    return len(residues)




def protein_coords(protein_accession):
    '''
    Getting protein coordinated from a pdb file.

    Args:
        protein_accession: Accession number of the protein to be searched

    Returns:
        A dataframe with 2 columns (accession, size) and 2 rows (the
        antitoxin and toxin) as well as the toxin and antitoxin accession
    '''
    
    # Get the structure file
    pdb_url, antitoxin, toxin, chain_colors = structure_file(protein_accession)

    # Read the pdb files
    pdb_parser = PdbParser(pdb_url)
    structure_data = pdb_parser.mol3d_data()

    # Get the lenght of the chains from the pdb file
    chain_a = count_residues(structure_data, 'A')
    chain_b = count_residues(structure_data, 'B')

    # Assign size to proper accession
    if protein_accession == antitoxin:
        data = {'accession': [antitoxin, toxin], 'size': [chain_a, chain_b]}
    elif protein_accession == toxin: 
        data = {'accession': [antitoxin, toxin], 'size': [chain_b, chain_a]}

    # Create a dataframe with the accession numbers and residue counts
    protein_coords_df = pd.DataFrame(data)

    return protein_coords_df, antitoxin, toxin




def protein_logos(relevant_domains_df, protein_db, accession):
    
    trace = go.Scatter(
        x=[],
        y=[],
        mode='markers',
        name=accession,
        marker=dict(
            size=10,
            color='blue' if accession == 'AAA' else 'red'
        )
    )

    # Add data to trace
    trace['x'].append(1)
    trace['y'].append(protein_db['size'][accession])
    for i, row in relevant_domains_df[relevant_domains_df['accession'] == accession].iterrows():
        database = row['database']
        domain_name = row['domain']
        domain_start = int(row['lenght'].split('-')[0])
        domain_end = int(row['lenght'].split('-')[1])
        domain_abundance = row['score']
        trace['x'].append(domain_start)
        trace['y'].append(protein_db['size'][accession])
        trace['x'].append(domain_end)
        trace['y'].append(protein_db['size'][accession])
        trace['text'] = f"{database} - {domain_name} ({domain_abundance})"

    # Create the plot
    data = [trace]
    layout = go.Layout(title=f"{accession} Domains", xaxis=dict(title='Domain Length'), yaxis=dict(title='Protein Size'))
    fig = go.Figure(data=data, layout=layout)
    
    return fig




def create_fig(protein_coords_df, relevant_domains_df, antitoxin, domain_color):
    
    # Trace lists
    arrowList = []
    domainList = []
    xList_gene = []
    yList_gene = []
    xList_domain = []
    yList_domain = []

    arrow_head = 15
    arrow_width = 1
    top_domain = 0.33
    top_domain_opacity = 0.7
    middle_domain = 0.33
    middle_domain_opacity = 0.7
    bottom_domain = 0.33
    bottom_domain_opacity = 0.5
    y_level_m = 0

    # 1. Merging the two traces into one plot
    fig = make_subplots(shared_yaxes=True, shared_xaxes=True)    

    # Create a trace for the accession
    for i, row in protein_coords_df.iterrows():
        if row['accession'] == antitoxin:
            protein_start = 1
            protein_end = (row['size'])/2
            x_axis = protein_end * 15

            xList_gene = [protein_start, protein_start, protein_end-arrow_head, protein_end, protein_end-arrow_head, protein_start]
            yList_gene = [y_level_m-arrow_width, y_level_m+arrow_width, y_level_m+arrow_width, y_level_m, y_level_m-arrow_width, y_level_m-arrow_width]
            arrowList.append(fig.add_trace(go.Scatter(x=xList_gene, y=yList_gene, fill="toself", fillcolor='#d9d9d9', opacity=0.5, line=(dict(color='#bfbfc0')), mode='lines+text')))

            for i, row in relevant_domains_df.iterrows():
                domain_protein = row['Accession']
                database = row['database']
                domain_name = row['domain']
                domain_start = int(row['temp_hmm'].split('-')[0])/2
                domain_end = int(row['temp_hmm'].split('-')[1])/2
                domain_size = domain_end - domain_start
                domain_abundance = row['score']
                domain_color = domain_color

                if database == 'pfam' and domain_protein == antitoxin:
                    y_level_d = y_level_m + 2
                    if antitoxin == domain_protein:
                        xList_domain = [domain_start, domain_start, protein_end-arrow_head, (protein_end-arrow_head) + (protein_end-domain_end), (protein_end-arrow_head) + (protein_end-domain_end), protein_end-arrow_head, domain_start]
                        yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d+top_domain/2,  y_level_d-top_domain/2, y_level_d-top_domain, y_level_d-top_domain]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain_name)))                                     

                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)
                
                elif database == 'cdd' and domain_protein == antitoxin:
                    y_level_d = y_level_m
                    if antitoxin == domain_protein:
                        xList_domain = [domain_start, domain_start, protein_end-arrow_head, (protein_end-arrow_head) + (protein_end-domain_end), (protein_end-arrow_head) + (protein_end-domain_end), protein_end-arrow_head, domain_start]
                        yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d+top_domain/2,  y_level_d-top_domain/2, y_level_d-top_domain, y_level_d-top_domain]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain_name)))                                     

                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)

                elif database == 'pdb' and domain_protein == antitoxin:
                    y_level_d = y_level_m - 2
                    if antitoxin == domain_protein:
                        xList_domain = [domain_start, domain_start, protein_end-arrow_head, (protein_end-arrow_head) + (protein_end-domain_end), (protein_end-arrow_head) + (protein_end-domain_end), protein_end-arrow_head, domain_start]
                        yList_domain = [y_level_d-top_domain, y_level_d+top_domain, y_level_d+top_domain, y_level_d+top_domain/2,  y_level_d-top_domain/2, y_level_d-top_domain, y_level_d-top_domain]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines', name = domain_name)))                                     

                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)

            # 9. Graph layout
            fig.update_xaxes(visible = False)
            fig.update_yaxes(
                visible = True, 
                showgrid = False, 
                showline = False, 
                autorange = True, 
                automargin = True, 
                showticklabels = False, 
                titlefont = dict(family = 'Open Sans', size = 8))
            fig.update_layout(
                autosize=False, 
                width=400, 
                height=300, 
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor = 'white', 
                plot_bgcolor = 'white', 
                showlegend = True
            )
            
    return fig



def create_protein_logos(protein_accession, include_pdb='no'):
    '''
    Drawing the logo for the antitoxin and toxin including the top 
    domains hit for pfam and cdd database.

    Args:
        protein_accession: Accession number of the protein to be searched
        include_pdb: If not None, the 
    Returns:
        A dataframe with 2 columns (accession, size) and 2 rows (the
        antitoxin and toxin) as well as the toxin and antitoxin accession    
    '''
    # Get the protein coords file, antitoxin, and toxin accession
    protein_coords_df, antitoxin, toxin = protein_coords(protein_accession)

    # Get the relevant domains
    if include_pdb == 'yes': 
        df_domains = df_domains_original
        df_domains = df_domains[df_domains['db_rank'] == 1]
    elif include_pdb == 'no':
        df_domains = df_domains_original[~df_domains_original['database'].str.contains('pdb')]
        df_domains = df_domains[df_domains['db_rank'] == 1]
    else:
        return print('Only acceptable strings are "yes" or "no"')
    
    # Fetch the relevant domains
    relevant_domains_df = find_domains(antitoxin, toxin, df_domains, 'Accession')

    # Drawing the antitoxin logo
    fig_antitoxin = create_fig(protein_coords_df, relevant_domains_df, antitoxin, 'green')

    # Drawing the toxin logo
    fig_toxin = create_fig(protein_coords_df, relevant_domains_df, toxin, 'red')

    return fig_antitoxin, fig_toxin
        
    
