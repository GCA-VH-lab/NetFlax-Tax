import pandas as pd
import requests
import dash
from urllib.request import urlopen
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide
from protein_coords import structure_file


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
    elif include_pdb == 'no':
        df_domains = df_domains
    else:
        return print('Only acceptable strings are "yes" or "no"')
    
    # Fetch the relevant domains
    relevant_domains_df = find_domains(antitoxin, toxin, df_domains, 'Accession')

    # Create the logos
    for i, row in relevant_domains_df.iterrows():
        



protein_coords('WP_093556480.1')
print('hej')