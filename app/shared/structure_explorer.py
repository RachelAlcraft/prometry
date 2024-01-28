import streamlit as st
from io import StringIO
from shared import config as cfg


def change():    
    st.session_state['ls_structures'] = []    
    st.session_state['df_geos'] = None

def explorer(no_geos=False,show_contacts=False):
    cfg.init()
    ls_structures = st.session_state['ls_structures']
    ls_geos = st.session_state['ls_geos']
        
    str_struc = " ".join(ls_structures)
    str_geo = " ".join(ls_geos)
    
    st.write("### Selection")
    sources = ["ebi","upload"]
    source = st.radio("Structure source", sources, index=0, on_change=change)    
                    
    if source == "upload":
        uploaded_file = st.file_uploader("Upload file in pdb or cif fomat",type=["pdb","cif"])
        if uploaded_file is not None:
            str_struc = uploaded_file.name.lower()
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()                        
            with open(f"{cfg.DATADIR}{str_struc}","w") as fw:
                fw.write(string_data)
                                    
    str_struc = st.text_input("Structures", value=str_struc,help="pdb/alphafold/user code",key="struc")
    if show_contacts:        
        str_contacts = st.text_input("Enter 2 contacts atoms",value="CA CA",help="space delim, 2 or 3 atoms - see help", key="ctcs")
        ls_cs = str_contacts.split(" ")
        str_geo = ls_cs[0] + "[aa|20]:{" + ls_cs[1] + "@i}[dis|0.5><10,rid|>1,aa|20]"

    if not no_geos:
        str_geo = st.text_input("Geometric parameters",value=str_geo,help="space delim, 2, 3 or 4 atoms - see help", key="geo")
    
    ls_structures = str_struc.split(" ")
    ls_geos = str_geo.split(" ")

    st.session_state['ls_structures'] = ls_structures
    st.session_state['ls_geos'] = ls_geos

    return ls_structures,ls_geos

def explorer_code():
    return ""

