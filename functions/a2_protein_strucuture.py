# VIUSALISING 3D PROTEIN STRUCTURES

# Imports
import pandas as pd
import dash
from io import StringIO
from dash_bio.utils import PdbParser, create_mol3d_style
from Bio.PDB import PDBParser, Polypeptide


# Import data
from data.data_prep import *

# Import functions
from functions.a1_protein_coords import *


def visualising_protein(search_term):
    '''
    Creates protein structure from a .pdb file

    Args:
        search_term: accession of the toxin/antitoxin
    
    Returns:
        structure_data: protein structure file
        styles: structure visualisation details
        chain_sequence: getting the chain structure
    '''    
    result = structure_file(search_term)
    pdb_file_url, antitoxin, toxin, chain_colors = result[:4]  # Assign first four values

    # Parsing the .pdb url link
    pdb_parser = PdbParser(pdb_file_url)

    # Getting structure data
    structure_data = pdb_parser.mol3d_data()

    # 
    chain_sequence = ''
    for chain in structure_data['atoms'][0]['chain']:
        if chain == antitoxin or chain == toxin:
            chain_sequence = Polypeptide.one_to_three(chain.get_sequence())
            break

    # Setting the style of the structure
    styles = create_mol3d_style(
        structure_data['atoms'], 
        visualization_type = 'cartoon', 
        color_element = 'chain',
        color_scheme = chain_colors
    )

    return structure_data, styles, chain_sequence




def generate_nglviewer(search_term, use_nglviewer=True):
    '''
    Creates protein structure from a .pdb file

    Args:
        search_term: accession of the toxin/antitoxin
        use_nglviewer: flag to indicate whether to use nglviewer for structure visualization
    
    Returns:
        structure_data: protein structure file
        styles: structure visualisation details
        chain_sequence: chain structure
    '''    
    result = structure_file(search_term)
    pdb_file_url, antitoxin, toxin, chain_colors = result[:4]  # Assign first four values

    # Parsing the .pdb url link
    pdb_parser = PdbParser(pdb_file_url)

    # Getting structure data
    structure_data = pdb_parser.mol3d_data()

    # 
    chain_sequence = ''
    for chain in structure_data['atoms'][0]['chain']:
        if chain == antitoxin or chain == toxin:
            chain_sequence = Polypeptide.one_to_three(chain.get_sequence())
            break

    # Setting the style of the structure
    styles = create_mol3d_style(
        structure_data['atoms'], 
        visualization_type='cartoon', 
        color_element='chain',
        color_scheme=chain_colors
    )

    if use_nglviewer:
        # Prepare structure data for NGLViewer
        nglviewer_data = {
            'atoms': structure_data['atoms'],
            'bonds': structure_data['bonds'],
            'metadata': structure_data['metadata'],
        }
        return nglviewer_data, styles, chain_sequence
    else:
        return structure_data, styles, chain_sequence





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