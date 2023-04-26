import pandas as pd
import requests
import dash
from dash_bio.utils import PdbParser, create_mol3d_style

# DATASET
def structure_file(protein_accession):
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
        pdb_url_new = f'http://130.235.240.53/NetFlax/T8_pdbs/{pdb_url}'
        #pdb_data = requests.get(pdb_url_new).text 
        #structure = pdb_parser.get_structure('myprotein', pdb_data)

    return pdb_url_new


accession = 'WP_110937839.1'
pdb_parser_at = PdbParser(structure_file(accession))

accession = 'WP_110937838.1'
pdb_parser_t = PdbParser(structure_file(accession))

print('Hi')