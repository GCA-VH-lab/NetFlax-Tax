# GETTING INFO ABOUT NETFLAX TAs

# Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup
import dash
from urllib.request import urlopen
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide
import time


# Import data
from data.data_prep import *


def structure_file(accession):
    '''
    Scans the server to find the .pdb file for the desired TA (based 
    on the toxin or antitoxin)

    Args:
        accession: accession of the toxin/antitoxin
    
    Returns:
        pdb_file: link to the pdb file containing the accession 
        antitoxin: antitoxin accession
        toxin: toxin accession 
        chain_colors: chain colors dictionary
        chain_a: accession number (either toxin or antitoxin)
        chain_b: accession number (either toxin or antitoxin)
    '''
    # URL of the server page
    url = 'http://130.235.240.53/NetFlax/T8_pdbs/'

    try:
        # Send a request to the server and retrieve the HTML content
        response = requests.get(url)
        html_content = response.text

        # Find the link to the PDB file in the HTML content
        pdb_url = ''
        soup = BeautifulSoup(html_content, 'html.parser')
        table_rows = soup.find_all('tr')
        for row in table_rows:
            columns = row.find_all('td')
            for col in columns:
                if col.a and accession in col.a.get('href', ''):
                    pdb_url = col.a.get('href', '')
                    break
            if pdb_url:
                break

        if pdb_url == '':
            error_message = 'Sorry, we could not locate the PDB file on our server.'
        else:
            pdb_file_url = f'http://130.235.240.53/NetFlax/T8_pdbs/{pdb_url}'
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
        if accession_chain in df_netflax['at_accession'].values:
            antitoxin = accession_chain
            toxin = complement_chain
            chain_a_color = 'lightgreen'
            chain_b_color = 'pink'
        elif accession_chain in df_netflax['t_accession'].values:
            toxin = accession_chain
            antitoxin = complement_chain
            chain_a_color = 'pink'
            chain_b_color = 'lightgreen'
        else:
            # Handle unexpected values in the DataFrame
            raise ValueError('Invalid DataFrame values')
        
        chain_colors = {'A': chain_a_color, 'B': chain_b_color}

        # Introduce a delay before returning the results
        time.sleep(1)  # Adjust the delay duration as needed
    
        return pdb_file_url, antitoxin, toxin, chain_colors, chain_a, chain_b

    except requests.exceptions.RequestException as e:
        error_message = f'Error occurred while accessing the server: {str(e)}'
        return print(error_message)