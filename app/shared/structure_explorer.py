import streamlit as st
from io import StringIO
from shared import config as cfg
import glob

def change():    
    pass
    #st.session_state['ls_structures'] = []    
    #st.session_state['str_structures'] = ""
    #st.session_state['df_geos'] = None

def explorer(use_geos="ordinary"):    
    cfg.init()
    ls_structures = st.session_state['ls_structures']
    ls_geos = st.session_state['ls_geos']
    ls_contacts = st.session_state['ls_contacts']
        
    str_struc = " ".join(ls_structures)
    str_geo = " ".join(ls_geos)
    str_contacts = " ".join(ls_contacts)
    
    st.write("### Selection")
    sources = ["keep selection", "enter pdbcodes","user uploaded","new upload"]
    source = st.radio("Structure source", sources, index=0, on_change=change,horizontal=True)
                    
    if source == "new upload":
        uploaded_file = st.file_uploader("Upload file in pdb or cif fomat",type=["pdb","cif","ent"])
        if uploaded_file is not None:
            str_struc = uploaded_file.name.lower()
            str_struc_name, str_struc_ext = str_struc.split(".")
            if str_struc_ext != "cif":
                str_struc_ext = "pdb"
            str_struc = f"user_{str_struc_name}.{str_struc_ext}"
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()                        
            with open(f"{cfg.DATADIR}{str_struc}","w") as fw:
                fw.write(string_data)                                    
    elif source == "user uploaded":
        user_files = glob.glob(f"{cfg.DATADIR}user_*")
        list_user = []        
        for uf in user_files:
            uff = uf.split("/")
            list_user.append((uff[-1]))
        selected_users = st.multiselect("Select one or more options:",list_user, key='option')
        if len(selected_users) > 0:
            str_struc = ""
            for su in selected_users:
                str_struc += su + " "
            str_struc = str_struc[:-1]    
    elif source == "enter pdbcodes":
        pass
        #str_struc = ""
    elif source == "keep selection":
        str_struc = st.session_state['str_structures']
    str_struc = st.text_input("Structures", value=str_struc,help="pdb/alphafold/user code",key="struc")
            
    if use_geos == "ordinary":
        str_geo = st.text_input("Geometric parameters",value=str_geo,help="space delim, 2, 3 or 4 atoms - see help", key="geo")    
    elif use_geos == "validation":
        val_geos = ["Ramachandran","N:CA","CA:C","C:O","C:N+1","C-1:N:CA","N:CA:C","CA:C:N+1","O:C:N+1"]
        str_geo = st.selectbox("Choose validation paramater",val_geos)
        if str_geo == "Ramachandran":
            str_geo = "C-1:N:CA:C N:CA:C:N+1"
    elif use_geos == "contacts":
        cols = st.columns(2)
        with cols[0]:
            str_contacts = st.text_input("Enter 2 contacts atoms",value="CA CA",help="space delim, 2 or 3 atoms - see help", key="ctcs")
            ls_cs = str_contacts.split(" ")
            str_geo = ls_cs[0] + "[aa|20]:{" + ls_cs[1] + "@i}[dis|0.5><10,rid|>1,aa|20]"
        with cols[1]:
            str_geo = st.text_input("Translated to geos =",value=str_geo,help="space delim, 2, 3 or 4 atoms - see help", key="geo")    
    
    ls_structures = str_struc.split(" ")
    ls_geos = str_geo.split(" ")

    if ls_geos != st.session_state['ls_geos']:        
        st.session_state['df_geos'] = None


    st.session_state['str_structures'] = str_struc
    st.session_state['ls_structures'] = ls_structures
    
    #if use_geos != "contacts":
    st.session_state['ls_geos'] = ls_geos
    
    return ls_structures,ls_geos

def explorer_code():
    return ""

