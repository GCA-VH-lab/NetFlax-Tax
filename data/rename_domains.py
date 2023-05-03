import pandas as pd


def rename_domains(domain_search_file, domain_annotations_file):
    '''
    Replaces the domain codes to domain names in the domain search file.
    
    Args:
        domain_search_file (pandas.DataFrame): The domain search file. 
            Note that the netflax_domain_search.csv used here has been 
            filtered and edited so the headers might not represent a 
            regular domain search output.
        domain_annotations_file (pandas.DataFrame): The domain 
            annotations file, as downloaded from HHPred.

    Returns:
        pandas.DataFrame: The domain search file but with domain names 
        instead of codes where this is applicable.
    '''
    # Creating a dictionary mapping domain codes to domain names
    domain_name_dict = dict(zip(domain_annotations_file.iloc[:, 0], domain_annotations_file.iloc[:, 1]))

    # Replace "PF" with "pfam" in the domain file
    domain_search_file['domain'] = domain_search_file['domain'].str.replace("PF", "pfam")

    handled_count = 0

    # Loop over domains in the domain file
    for i, domain in domain_search_file['domain'].items():
        if domain:
            domain_code = domain.split('.')[0]
            domain_name = domain_name_dict.get(domain_code)
            if domain_name:
                domain_search_file.at[i, 'domain'] = domain.replace(domain_code, domain_name)
                handled_count += 1
            else:
                print(f"No domain name found for code {domain_code}")
        else:
            print(f"Empty domain for row {i}")
                
    print(f"{handled_count} domains handled")
    print(f"{domain_search_file['domain'].notnull().sum()} domains remaining")

    with open('domains.txt', 'w') as f:
        f.write(domain_search_file.to_string(index = False))
        print('New file "domains.txt" is ready')

    return domain_search_file


# 1. The two dataasets to be used
domain_search = pd.read_csv('./data/netflax_domain_search.csv', sep = '\t', header = 0)
domain_annotations = pd.read_csv('./data/domain_annotations_map.txt', sep = '\t')


# 2. Run the function and output the new file as domains.txt
df = rename_domains(domain_search, domain_annotations)
df.to_csv('domains.txt', sep='\t', index=False)