# NetFlax Tax 
A visualisation application allowing the user to view protein structures and filter the predicted NetFlax toxin-antitoxin pairs based on taxonomy, nodes, or accession number. 
<img width="1440" alt="Screenshot 2023-06-26 at 23 59 01" src="https://github.com/vedabojar/NetFlax-Stats/assets/100831180/21887b13-db08-4218-843f-4f01052c0ef3">

### Output Example
<img width="1439" alt="Screenshot 2023-06-27 at 08 44 29" src="https://github.com/vedabojar/NetFlax-Stats/assets/100831180/293ea6b3-abcb-45f7-88d6-e2137f85847d">

## Setting Up

### How to run
1. Clone the repository to your local machine:
```
git clone https://github.com/vedabojar/NetFlax-Tax.git
```

2. Navigate to the directory containing the program
```
cd NetFlax-Tax
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the program:
```
python app.py
```


### Folder structure

```
|- README.md
|- app.py
|- callbacks.py
|- index.py
|- requirements.txt
|- wsgi.py
├── assets
│   ├──color_scheme.py
│   ├──index.css
│   ├──table.css
│   └──download_button.css
├── data
│   ├──data_prep.py
│   ├──rename_domains.py
│   ├──netflax_dataset.xlsx
│   ├──netflax_domain_search.csv
│   ├──domains.txt
│   └──domain_annotation_map.txt
├── functions
│   ├──a1_protein_coords.py
│   ├──a2_protein_coords.py
│   ├──a3_create_logos.py
│   ├──b1_table.py
│   ├──b2_sunburst_fig.py
│   └──b3_download_dataset.py
├── pages
│   ├──home.py
│   └──navigation.py
├── images
│   ├──app_logo.png
│   └──favicon.ico
└── .gitignore
```

