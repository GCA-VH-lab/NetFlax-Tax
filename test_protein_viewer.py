import pandas as pd
import requests
import dash

from dash import Dash, html, dash_table
from dash.dependencies import Input, Output
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
import pandas as pd



# ----------------------- ACCESSING SERVER DATA ------------------------

# Reads the queueDir HTML and retrives the runs and dates

#storred_structures = 'http://130.235.240.53/NetFlax/T8_pdbs/'
accession = 'WP_041839411.1-WP_148215087.1'

def structure_file(s):
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


# -------------------------- PROTEIN VIEWER ----------------------------

app = dash.Dash(__name__)

pdb_parser = PdbParser(structure_file(accession))
data = pdb_parser.mol3d_data()

# Create molecule viewer
styles = create_mol3d_style(
    data['atoms'], visualization_type='cartoon', color_element='chain'
)

app.layout = html.Div([
    dashbio.Molecule3dViewer(
        id='dashbio-default-molecule3d',
        modelData=data,
        styles=styles
    ),
    "Selection data",
    html.Hr(),
    html.Div(id='default-molecule3d-output')
])

@app.callback(
    Output('default-molecule3d-output', 'children'),
    Input('dashbio-default-molecule3d', 'selectedAtomIds')
)
def show_selected_atoms(atom_ids):
    if atom_ids is None or len(atom_ids) == 0:
        return 'No atom has been selected. Click somewhere on the molecular \
        structure to select an atom.'
    return [html.Div([
        html.Div('Element: {}'.format(data['atoms'][atm]['elem'])),
        html.Div('Chain: {}'.format(data['atoms'][atm]['chain'])),
        html.Div('Residue name: {}'.format(data['atoms'][atm]['residue_name'])),
        html.Br()
    ]) for atm in atom_ids]

if __name__ == '__main__':
    app.run_server(debug=True)
