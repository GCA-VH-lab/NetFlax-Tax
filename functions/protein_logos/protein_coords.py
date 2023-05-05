import pandas as pd
import requests
import dash
from urllib.request import urlopen
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide


# DATASET
df_netflax = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')


def structure_file(accession):
    '''
    Uses the URL to operon file to check if the URL is accessible 
    (i.e if the submission is still stored).
    '''
    # URL of the server page
    url = 'http://130.235.240.53/NetFlax/T8_pdbs/'

    # Send a request to the server and retrieve the HTML content
    response = requests.get(url)
    html_content = response.text

    # Find the link to the PDB file in the HTML content
    pdb_url = None
    for line in html_content.split('\n'):
        if '<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href=' in line and accession in line:
            pdb_url = line.split('href=')[1].split('"')[1]
            break

    if pdb_url is None:
        print('No PDB file found on the server page.')
    else:
        pdb_file = f'http://130.235.240.53/NetFlax/T8_pdbs/{pdb_url}'
        chain_a = pdb_url.split('-')[0]
        chain_b = pdb_url.split('-')[1].split('.pdb')[0]

    # Set default chain colors
    chain_a_color = 'gray'
    chain_b_color = 'gray'

    # Initialize accession_chain and complement_chain with default values
    accession_chain = None
    complement_chain = None

    # Assign accessions and complementary chains
    if accession == chain_a:
        accession_chain = accession
        complement_chain = chain_b
    elif accession == chain_b:
        accession_chain = accession
        complement_chain = chain_a
    else:
        # Handle unexpected accession values
        raise ValueError('Invalid accession')

    # Determine antitoxin and toxin based on accession and complementary chain
    if accession in df_netflax['at_accession'].values:
        antitoxin = accession_chain
        toxin = complement_chain
        chain_a_color = 'lightgreen'
        chain_b_color = 'pink'
    elif complement_chain in df_netflax['t_accession'].values:
        toxin = accession_chain
        antitoxin = complement_chain
        chain_a_color = 'pink'
        chain_b_color = 'lightgreen'
    else:
        # Handle unexpected values in the DataFrame
        raise ValueError('Invalid DataFrame values')
    
    chain_colors = {'A': chain_a_color,'B': chain_b_color,}

    return pdb_file, antitoxin, toxin, chain_colors


def visualising_protein(search_term):
    pdb_url, antitoxin, toxin, chain_colors = structure_file(search_term)
    pdb_parser = PdbParser(pdb_url)
    structure_data = pdb_parser.mol3d_data()

    chain_sequence = ""
    for chain in structure_data['atoms'][0]['chain']:
        if chain == antitoxin or chain == toxin:
            chain_sequence = Polypeptide.one_to_three(chain.get_sequence())
            break

    styles = create_mol3d_style(
        structure_data['atoms'], 
        visualization_type = 'cartoon', 
        color_element = 'chain',
        color_scheme = chain_colors
    )

    return structure_data, styles, chain_sequence