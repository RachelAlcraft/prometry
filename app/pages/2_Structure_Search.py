import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px
import requests

DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - structure search")
st.write("This tool finds solved or predicted structures for a given gene in the human taxon 9606")
st.write("It is intended to simplify the use of this webapp by making it easier to obtain structures")

code_string = "from prometry import pdbloader as pl\n"
code_string += "from prometry import pdbgeometry as pg\n"
code_string += "import pandas as pd\n"
code_string += "import requests\n"
code_string += f"DATADIR = '{DATADIR}'\n"

code_string2 = ""



tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:

    if 'gene' not in st.session_state:
        st.session_state['gene'] = ""    
    if 'code_gene' not in st.session_state:
        st.session_state['code_gene'] = ""

    cols = st.columns([1,1,1])
    with cols[0]:
        gene = st.text_input("Gene", value="BRCA1")                    
        url = f"https://rest.uniprot.org/uniprotkb/search?query=reviewed:true+AND+organism_id:{9606}+AND+gene_exact:{gene}"
    with cols[1]:
        # https://www.uniprot.org/uniprotkb?query=(reviewed:true)%20AND%20(organism_id:9606)%20AND%20(gene:BRCA1)        
        st.write(f"[Uniprot api call]({url})")
        
    code_string += f"ra = requests.get(url='{url}')"
    code_string += """
accessions = []
pdbs = []
data = ra.json()
if len(data["results"]) > 0:
    for dt in data["results"]:
        accession = dt["primaryAccession"]
        accessions = dt["secondaryAccessions"]
accessions.insert(0, accession)     
pdbs.insert(0, f"AF-{accession}-F1-model_v4")   

res = data["results"][0]["uniProtKBCrossReferences"]
for x in res:
    db = x["database"]
    pdb = x["id"]
    if db == "PDB":
        pdbs.append(pdb)
        """

    accessions = []
    accession = ""
    pdbs = ""

    ra = requests.get(url=url)
    data = ra.json()
    if len(data["results"]) > 0:
        for dt in data["results"]:
            accession = dt["primaryAccession"]            
            accessions = dt["secondaryAccessions"]
        accessions.insert(0, accession)
        
        res = data["results"][0]["uniProtKBCrossReferences"]
        for x in res:
            db = x["database"]
            pdb = x["id"]
            if db == "PDB":
                pdbs += pdb + " "


                
    if accession != "":
        st.text_input("AplhaFold structure", f"AF-{accession}-F1-model_v4")
        st.text_input("PDB Structures", pdbs[:-1])
    else:
        st.write("No accession code found")
    
    st.session_state['code_gene'] = code_string

with tabCode:
    st.code(st.session_state['code_gene'])
    