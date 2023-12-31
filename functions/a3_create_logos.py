# FUNCTIONS FOR CREATING LOGOS

# Imports 
import pandas as pd
import requests
import dash
from urllib.request import urlopen
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Import data
from data.data_prep import *

# Import functions
from functions.a1_protein_coords import *
from functions.a2_protein_strucuture import *

# Import aesthetetics
from assets.color_scheme import *



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
    
    return filtered_df





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
    pdb_file_url, antitoxin, toxin, chain_colors, chain_a, chain_b = structure_file(protein_accession)

    # Read the pdb files
    pdb_parser = PdbParser(pdb_file_url)
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

    return protein_coords_df, antitoxin, toxin




def create_fig(protein_coords_df, relevant_domains_df, antitoxin, domain_color):
    '''
    Creating a protein logo figure including the domain inside it.

    Args:
        protein_coords_df: Coordinates of the protien
        relevan_domains_df: Dataframe with only the domains found in the
            the protein of interest
        antitoxin: Antitoxin accession
        domain_color: color of the domain

    Returns:
        Returns a figure (graph) with protein and and its domains
    '''

    # Lists to store shape specifics
    arrowList = []
    domainList = []
    xList_gene = []
    yList_gene = []
    xList_domain = []
    yList_domain = []

    # Factors to set correct arrow size
    divide_by = 10
    factor_length = 1
    arrow_width = 3/divide_by

    # The placement of the arrow along the y axis
    y_level = 0

    # Domain color opacity
    domain_opacity = 0.7


    # Merging the two traces (protein + domain) into one plot
    fig = make_subplots(shared_yaxes=True, shared_xaxes=True)    

    # Create a trace for the accession
    for i, row in protein_coords_df.iterrows():
        if row['accession'] == antitoxin:
            # Extracting coordinates
            protein_start = 1
            protein_end = (row['size'])*factor_length
            arrow_head = ((protein_end-protein_start)*(1/8))*factor_length
            
            # Setting shape specifics
            xList_gene = [protein_start, protein_start, protein_end-arrow_head, protein_end, protein_end-arrow_head, protein_start]
            yList_gene = [y_level-arrow_width, y_level+arrow_width, y_level+arrow_width, y_level, y_level-arrow_width, y_level-arrow_width]
            arrowList.append(fig.add_trace(go.Scatter(x=xList_gene, y=yList_gene, fill="toself", fillcolor='#d9d9d9', opacity=0.5, line=(dict(color='#bfbfc0')), mode='lines+text')))

            # Iterate through the domain data and get info for domains
            for i, row in relevant_domains_df.iterrows():
                domain_protein = row['Accession']
                database = row['database']
                domain_name = row['domain']
                domain_start = int(row['query_hmm'].split('-')[0]) * factor_length
                domain_end = int(row['query_hmm'].split('-')[1]) * factor_length
                domain_size = (domain_end - domain_start) * factor_length
                domain_score = row['score']
                domain_color = domain_color

                if antitoxin == domain_protein:  
                    if domain_end > arrow_head:
                        # Domain ends in the arrow head area
                        xList_domain = [domain_start, domain_start, protein_end-arrow_head, (protein_end-arrow_head) + (protein_end-domain_end), (protein_end-arrow_head) + (protein_end-domain_end), protein_end-arrow_head, domain_start]
                        yList_domain = [y_level-arrow_width, y_level+arrow_width, y_level+arrow_width, y_level+arrow_width,  y_level-arrow_width, y_level-arrow_width, y_level-arrow_width]  
                        arrowList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo='none', fillcolor=domain_color, line=dict(color=domain_color, width=0), opacity=domain_opacity, mode='lines', name=domain_name)))
                    else:
                        # Domain does not end in the arrow head area
                        xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                        yList_domain = [y_level - arrow_width, y_level + arrow_width, y_level + arrow_width, y_level - arrow_width, y_level - arrow_width]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo='none', fillcolor=domain_color, line=dict(color=domain_color, width=0), opacity=domain_opacity, mode='lines', name=domain_name)))


                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level+0.5, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)

            # Graph specifics
            fig.update_xaxes(
                visible = False,
                zeroline = False
            )
            fig.update_yaxes(
                visible = True, 
                showgrid = False, 
                showline = False,
                range = [-2, 2], 
                automargin = True, 
                showticklabels = False, 
                zeroline=False,
                titlefont = dict(family = font_family, size = 8))
            fig.update_layout(
                autosize=False, 
                width=200, 
                height=200, 
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
        protein_accession: Accession number of the protein to be 
            searched
    Returns:
        Logo figure of the toxin and antitoxin   
    '''
    # Get the protein coords file, antitoxin, and toxin accession
    protein_coords_df, antitoxin, toxin = protein_coords(protein_accession)

    # Get the relevant domains
    df_domains = df_domains_original[df_domains_original['Accession'].isin([antitoxin, toxin])]
    
    # Find the index of the rows with the highest 'prob' value for each 'acc'
    highest_prob_rows = df_domains.groupby('Accession')['prob'].idxmax()
    df_top_domains = df_domains.loc[highest_prob_rows]

    # Fetch the relevant domains
    relevant_domains_df = find_domains(antitoxin, toxin, df_top_domains, 'Accession')

    # Drawing the antitoxin logo
    fig_antitoxin = create_fig(protein_coords_df, relevant_domains_df, antitoxin, antitoxin_color)

    # Drawing the toxin logo
    fig_toxin = create_fig(protein_coords_df, relevant_domains_df, toxin, toxin_color)

    return fig_antitoxin, fig_toxin
        
    

# Test it out 
# create_protein_logos('WP_013360663.1', 'yes')
