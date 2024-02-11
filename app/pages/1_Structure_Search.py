import streamlit as st
import requests
import pandas as pd

DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)





st.header("Prometry - Structure Search")
st.caption('''
"For certain types of important digital objects, there are well-curated, deeply-integrated, special-purpose repositories such as Genbank3, 
Worldwide Protein Data Bank (wwPDB4), and UniProt5 in the life sciences ... These foundational and critical core resources are continuously 
curating and capturing high-value reference datasets and fine-tuning them to enhance scholarly output, provide support for both 
human and mechanical users, and provide extensive tooling to access their content in rich, dynamic ways."(Wilkinson et al, 2016)
''')
st.write("""
This tool finds solved or predicted structures for a given gene and taxon (human is 9606). 
It facilitates further use of this webapp by making it easier to obtain structures (but you can type in any that you like).  
""")

code_string = "import requests\n"

code_string2 = ""



tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:

    if 'gene' not in st.session_state:
        st.session_state['gene'] = ""    
    if 'code_gene' not in st.session_state:
        st.session_state['code_gene'] = ""

    cols = st.columns([1,1,1,1])
    with cols[0]:
        gene = st.text_input("Gene", value="BRCA1")                    
    with cols[1]:
        taxon = st.text_input("Taxon", value="9606") 
        url = f"https://rest.uniprot.org/uniprotkb/search?query=reviewed:true+AND+organism_id:{taxon}+AND+gene_exact:{gene}"
    with cols[2]:        
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

    if st.button("Find structures"):
        accessions = []
        accession = ""
        pdbs = ""
        pdbls = []
        pdb_dict = {}
        count = 0
        #pdb_dict["index"] = []
        pdb_dict["pdb"] = []
        pdb_dict["link"] = []
        #pdb_dict["jmol_link"] = []
        pdb_dict["method"] = []
        pdb_dict["resolution"] = []
        pdb_dict["chains"] =  []
        pdb_dict["residues"] =  []

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
                props = x["properties"]
                
                if db == "PDB":
                    #print(pdb,method,reso,x)

                    method, reso,chains, residues = "","","",""
                    for prop in props:
                        if prop["key"] == "Method":
                            method= prop["value"]
                        elif prop["key"] == "Resolution":
                            reso = prop["value"]
                        elif prop["key"] == "Chains":
                            chains = prop["value"].split("=")[0]
                            residues = prop["value"].split("=")[1]

                    pdbs += f"{pdb} "
                    pdbls.append((pdb,method,reso,chains))
                    #pdb_dict["index"].append(count)
                    pdb_dict["pdb"].append(pdb)
                    pdb_dict["link"].append(f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb}")
                    #pdb_dict["jmol_link"].append(f"https://proteopedia.org/wiki/fgij/fg.htm?mol={pdb}")                    
                    pdb_dict["method"].append(method)
                    pdb_dict["resolution"].append(str(reso))
                    pdb_dict["chains"].append(chains)
                    pdb_dict["residues"].append(residues)
                    count += 1
                                    
        if len(accession) > 0:
            cols = st.columns(3)    
            for acc in accessions:        
                af_pdb = f"AF-{acc}-F1-model_v4"
                af_url = f"https://alphafold.ebi.ac.uk/files/{af_pdb}.pdb"
                response = requests.get(af_url)
                if response.status_code == 200:
                    with cols[0]:
                        st.text_input("AplhaFold structure", af_pdb)
                    with cols[1]:
                        st.write(".")
                        st.write(f"[AlphaFold {acc}](https://alphafold.ebi.ac.uk/entry/{acc})")                            
                        break
                else:
                    st.warning(f'{af_url} does not exist')
            with st.expander("Expand accessions"):
                st.write(accessions)
                
            st.text_input("PDB Structures", pdbs[:-1])

            df = pd.DataFrame()
            if count > 0:
                df = pd.DataFrame.from_dict(pdb_dict)
            st.data_editor(
            df,
            column_config={
                "link": st.column_config.LinkColumn("link")
            },
            hide_index=True,
            )
        else:
            st.write("No structures found")


        st.session_state['code_gene'] = code_string

with tabCode:
    st.code(st.session_state['code_gene'])


st.divider()
st.caption("""Garcia, L., Bolleman, J., Gehant, S., Redaschi, N., Martin, M., UniProt Consortium, Bateman, A., 
Magrane, M., Martin, M., Orchard, S., Raj, S., Ahmad, S., Alpi, E., Bowler, E., Britto, R., 
Bursteinas, B., Bye-A-Jee, H., Dogan, T., Garcia, L., … Zhang, J. (2019). 
FAIR adoption, assessment and challenges at UniProt. Scientific Data, 6(1), 175. https://doi.org/10.1038/s41597-019-0180-9""")

st.caption("""Wilkinson, M. D., Dumontier, M., Aalbersberg, Ij. J., Appleton, G., Axton, M., Baak, A., Blomberg, N., Boiten, J.-W., da Silva Santos, 
L. B., Bourne, P. E., Bouwman, J., Brookes, A. J., Clark, T., Crosas, M., Dillo, I., Dumon, O., Edmunds, S., Evelo, C. T., Finkers, R., … Mons, B. (2016). 
The FAIR Guiding Principles for scientific data management and stewardship. Scientific Data, 3(1), 160018. https://doi.org/10.1038/sdata.2016.18""")
