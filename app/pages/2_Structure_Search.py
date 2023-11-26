import streamlit as st
import requests

DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - structure search")
st.caption('''
"UniProt data are published via a website (https://www.uniprot.org/uniprot) and distributed in multiple serialization formats, 
including a custom text format, XML, RDF/XML and FASTA. In addition, 
we also provide Application Programming Interfaces (API)s and File Transfer Protocol (FTP) downloads."(Garcia et al, 2019)
''')
st.write("""
This tool finds solved or predicted structures for a given gene in the human taxon 9606.  It simplifies the use of this webapp by making it easier to obtain structures (but you can type in any that you like).  
""")

code_string = "import requests\n"

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
        st.write(".")
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
print(accessions)
print(pdbs)
        """

    accessions = []
    accession = ""
    pdbs = ""
    pdbls = []

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
                pdbls.append(pdb)


                
    if accession != "":
        cols = st.columns(3)
        with cols[0]:
            st.text_input("AplhaFold structure", f"AF-{accession}-F1-model_v4")
        with cols[1]:
            st.write(".")
            st.write(f"[AlphaFold {accession}](https://alphafold.ebi.ac.uk/entry/{accession})")
        st.text_input("PDB Structures", pdbs[:-1])
        st.write("PDB Links")        
        cols = st.columns(6)
        for i in range(len(pdbls)):
            pdb = pdbls[i]
            with cols[i%4]:
                st.write(f"[{pdb}](https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb})")
            
    else:
        st.write("No accession code found")
    
    st.session_state['code_gene'] = code_string

with tabCode:
    st.code(st.session_state['code_gene'])


st.divider()
st.caption("Garcia, L., Bolleman, J., Gehant, S., Redaschi, N., Martin, M., UniProt Consortium, Bateman, A., Magrane, M., Martin, M., Orchard, S., Raj, S., Ahmad, S., Alpi, E., Bowler, E., Britto, R., Bursteinas, B., Bye-A-Jee, H., Dogan, T., Garcia, L., … Zhang, J. (2019). FAIR adoption, assessment and challenges at UniProt. Scientific Data, 6(1), 175. https://doi.org/10.1038/s41597-019-0180-9")
    