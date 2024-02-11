import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
from shared import config as cfg

DATADIR = "app/data/"
PERFECT_PDB = "4rek"

#--------------------------------------------------------------------
def load_pdbs(ls_structures):
    pobjs = []                            
    cif = False
    for pdb in ls_structures:        
        try:
            if "AF-" in pdb:
                source = "alphafold"
            else:
                source = "ebi"
                pdb = pdb.lower()
            if "." in pdb:
                pdb,ext = pdb.split(".")
                if ext == "cif":
                    cif = True
            pla = pl.PdbLoader(pdb,DATADIR,cif=cif,source=source)        
            po = pla.load_pdb()
            pobjs.append(po)
        except Exception as e:
            st.error(str(e))
    return pobjs
#--------------------------------------------------------------------
def maker_geos(ls_structures, ls_geos, extra_underlying=False):
    cfg.init()
    df_geos = st.session_state['df_geos']
    df_geos_xtra = st.session_state['df_geos_xtra']
    if len(ls_structures) == 0 or len(ls_geos) == 0 or len(ls_structures[0]) == 0:
        st.write("No structures entered")
    else:        
        st.write("### Calculation")        
        if st.button("Calculate dataframe"):                    
            pobjs = load_pdbs(ls_structures)                        
            gm = pg.GeometryMaker(pobjs)
            df_geos = gm.calculateGeometry(ls_geos)
            if extra_underlying:
                pobjs_xtra = load_pdbs([PERFECT_PDB])
                gm_xtra = pg.GeometryMaker(pobjs_xtra)
                df_geos_xtra = gm_xtra.calculateGeometry(ls_geos)                                                                                 
                st.session_state['df_geos_xtra'] = df_geos_xtra
        if df_geos is not None and len(df_geos.index) > 0:                            
            with st.expander("Expand geometric dataframe"):
                st.dataframe(df_geos)
    st.session_state['df_geos'] = df_geos    
    if extra_underlying:
        return df_geos,df_geos_xtra
    else:
        return df_geos
#--------------------------------------------------------------------
def maker_atoms(ls_structures):
    cfg.init()
    df_atoms = st.session_state['df_atoms']
    if len(ls_structures) == 0 or len(ls_structures[0]) == 0:
        st.write("No structures entered")
    else:        
        st.write("### Calculation")        
        if st.button("Calculate dataframe"):                    
            pobjs = load_pdbs(ls_structures)                        
            gm = pg.GeometryMaker(pobjs)
            df_atoms = gm.calculateData()
                                                                                             
        if df_atoms is not None and len(df_atoms.index) > 0:                            
            with st.expander("Expand (x,y,z) dataframe"):
                st.dataframe(df_atoms)
            df_atoms = df_atoms.rename(columns={"pdbCode":"pdb_code"})
    st.session_state['df_atoms'] = df_atoms
    return df_atoms

#--------------------------------------------------------------------



#--------------------------------------------------------------------




#--------------------------------------------------------------------