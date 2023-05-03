import pandas as pd
import requests
import dash
from urllib.request import urlopen
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide


# DATASETS
df_all = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='01_searched_genomes')
df_netflax = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='02_netflax_predicted_tas')
df_domains_original = pd.read_csv('./data/domains.txt', sep = '\t', header = 0)

# Filtering out the pdb rows of the domains file
df_domains = df_domains_original[~df_domains_original['database'].str.contains('pdb')]   # NOTE! pdb domain searches are ignored


def find_domains(antitoxin, toxin, dataset):
    '''
    Find the domains of the specified antitoxin and toxin proteins.

    Args:
        antitoxin: Accession number of the antitoxin protein.
        toxin: Accession number of the toxin protein.
        dataset

    Returns:
        A subset of the domain search file containing the domains 
        associated with the specified antitoxin and toxin proteins.
    '''
    



print('hej')