# PREPING DATABASES

# Imports
import pandas as pd



# All TA searches
df_all = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='2. Searched Genomes')

# Only NetFlax TAs
df_netflax = pd.read_excel('./data/netflax_dataset.xlsx', engine='openpyxl', sheet_name='3. NetFlax Predicted TAs')

# Domains found in all NetFlax TAs for 3 databases
df_domains_original = pd.read_csv('./data/domains.txt', sep = '\t', header = 0)

# Domains found in all NetFlax TAs for 2 databases (no PDB)
df_domains = df_domains_original[~df_domains_original['database'].str.contains('pdb')]   # NOTE! pdb domain searches are ignored

