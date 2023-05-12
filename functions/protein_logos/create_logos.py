import pandas as pd
import requests
import dash
from urllib.request import urlopen
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide
from functions.protein_logos.protein_coords import *
#from protein_coords import structure_file, visualising_protein
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# --------------------------- LAYOUT SPEC ------------------------------

page_background = '#F6F6F6'
container_background = '#ECECEC'
transparent_background = 'rgba(0,0,0,0)'

# Visualistions colors
antitoxin_color = 'darkgreen'
toxin_color = 'darkred'
wedge_non_highlight = '#6d8aa6'
wedge_highlight = '#6d8aa6'



# ---------------------------- DATASETS --------------------------------

df_all = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')
df_domains_original = pd.read_csv('./data/domains.txt', sep = '\t', header = 0)

# Filtering out the pdb rows of the domains file
df_domains = df_domains_original[~df_domains_original['database'].str.contains('pdb')]   # NOTE! pdb domain searches are ignored



# ---------------------------- FUNCTIONS -------------------------------

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
    pdb_url, antitoxin, toxin, chain_colors, chain_a, chain_b = structure_file(protein_accession)

    # Read the pdb files
    pdb_parser = PdbParser(pdb_url)
    structure_data = pdb_parser.mol3d_data()

    # Get the lenght of the chains from the pdb file
    chain_a_size = count_residues(structure_data, 'A')
    chain_b_size = count_residues(structure_data, 'B')

    # Assign size to proper accession
    if protein_accession == chain_a:
        data = {'accession': [antitoxin, toxin], 'size': [chain_a_size, chain_b_size]}
    elif protein_accession == toxin: 
        data = {'accession': [antitoxin, toxin], 'size': [chain_b_size, chain_a_size]}

    # Create a dataframe with the accession numbers and residue counts
    protein_coords_df = pd.DataFrame(data)
    print('WP_181273885.1')

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

    divide_by = 10
    factor_length = 1

    arrow_width = 3/divide_by

    y_level = 0

    domain_opacity = 0.7

    # 1. Merging the two traces into one plot
    fig = make_subplots(shared_yaxes=True, shared_xaxes=True)    

    # Create a trace for the accession
    for i, row in protein_coords_df.iterrows():
        if row['accession'] == antitoxin:
            protein_start = 1
            protein_end = (row['size'])*factor_length
            arrow_head = ((protein_end-protein_start)*(1/8))*factor_length

            xList_gene = [protein_start, protein_start, protein_end-arrow_head, protein_end, protein_end-arrow_head, protein_start]
            yList_gene = [y_level-arrow_width, y_level+arrow_width, y_level+arrow_width, y_level, y_level-arrow_width, y_level-arrow_width]
            arrowList.append(fig.add_trace(go.Scatter(x=xList_gene, y=yList_gene, fill="toself", fillcolor='#d9d9d9', opacity=0.5, line=(dict(color='#bfbfc0')), mode='lines+text')))

            for i, row in relevant_domains_df.iterrows():
                domain_protein = row['Accession']
                database = row['database']
                domain_name = row['domain']
                domain_start = (row['query_hmm'].split('-')[0])*factor_length
                domain_end = int(row['query_hmm'].split('-')[1])*factor_length
                domain_size = (domain_end - domain_start)*factor_length
                domain_score = row['score']
                domain_color = domain_color

                if antitoxin == domain_protein:
                    xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                    yList_domain = [y_level-arrow_width, y_level+arrow_width, y_level+arrow_width, y_level-arrow_width, y_level-arrow_width]
                    domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = domain_opacity, mode='lines', name = domain_name)))                                     

                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)

            # 9. Graph layout
            fig.update_xaxes(visible = False)
            fig.update_yaxes(
                visible = True, 
                showgrid = False, 
                showline = False,
                range = [-2, 2], 
                automargin = True, 
                showticklabels = False, 
                titlefont = dict(family = 'Open Sans', size = 8))
            fig.update_layout(
                autosize=False, 
                width=300, 
                height=300, 
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor = transparent_background, 
                plot_bgcolor = transparent_background, 
                showlegend = False
            )
            
    return fig



def create_protein_logos(protein_accession):
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
    protein_coords_df, antitoxin, toxin, chain_a, chain_b = protein_coords(protein_accession)

    # Get the relevant domains
    df_domains = df_domains_original[df_domains_original['Accession'].isin([antitoxin, toxin])]
    
    # Find the index of the rows with the highest 'prob' value for each 'acc'
    highest_prob_rows = df_domains.groupby('Accession')['prob'].idxmax()
    df_top_domains = df_domains.loc[highest_prob_rows]


    # Fetch the relevant domains
    relevant_domains_df = find_domains(antitoxin, toxin, df_top_domains, 'Accession')

    # Drawing the antitoxin logo
    fig_antitoxin = create_fig(protein_coords_df, relevant_domains_df, antitoxin, 'green')

    # Drawing the toxin logo
    fig_toxin = create_fig(protein_coords_df, relevant_domains_df, toxin, 'red')

    fig_antitoxin.show()
    fig_toxin.show()

    return fig_antitoxin, fig_toxin
        
    

# create_protein_logos('WP_013360663.1', 'yes')
