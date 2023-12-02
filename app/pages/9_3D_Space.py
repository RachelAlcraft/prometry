import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px

DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)
st.header("Atoms in 3d space ")
st.caption('''
"Here we shall use the term 'protein structure' in an entirely different sense... Whereas Anfinsen and Redfield have concerned themselves 
with the amino acid sequence and topological interconnections of the polypeptide chains, we shall consider mainly the geometrical 
aspects - the arrangement of the atoms in space."(Crick&Kendrew, 1957)
''')
st.write("""
The AlphaFold TP53 predicted structure is the default, showing the characteristic predictive format of a high plDDT core 
where there are solved structures, with hightly uncertain regions at the edges.
""")

code_string = "from prometry import pdbloader as pl\n"
code_string += "from prometry import pdbgeometry as pg\n"
code_string += "import pandas as pd\n"
code_string += f"DATADIR = '{DATADIR}'\n"

code_string2 = ""



tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:

    if 'pdbs' not in st.session_state:
        st.session_state['pdbs'] = ""
    if 'geos' not in st.session_state:
        st.session_state['geos'] = ""
    if 'code_df' not in st.session_state:
        st.session_state['code_df'] = ""
        st.session_state['code_df2'] = ""        

    
    st.write("##### Edit/enter structures")

    structures = "AF-P04637-F1-model_v4"
            
    cols = st.columns([1,1])
    with cols[0]:
        structures = st.text_input("List of structures", value=structures,help="pdb or alphafold codes, space delim")

    ls_structures = structures.split(" ")
        
    df_atoms = pd.DataFrame({'A' : []})
    if 'atoms' not in st.session_state:        
        st.session_state['atoms'] = df_atoms
    else:
        if st.session_state['pdbs'] != structures:            
            st.session_state['atoms'] = df_atoms
            st.session_state['pdbs'] = structures            
        else:            
            df_atoms = st.session_state['atoms']
    
    st.write("---")
    st.write("##### Calculate dataframe")
    if st.button("Calculate dataframe"):

        code_string += f"ls_structures = {ls_structures}\n"                
        pobjs = []
        code_string += f"for pdb in ls_structures:"
        code_string += """    
        if "AF-" in pdb:
            source = "alphafold"
        else:
            source = "ebi"
            pdb = pdb.lower()
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source=source)        
        po = pla.load_pdb()
        pobjs.append(po)
        """                
        for pdb in ls_structures:        
            if "AF-" in pdb:
                source = "alphafold"
            else:
                source = "ebi"
                pdb = pdb.lower()
            pla = pl.PdbLoader(pdb,DATADIR,cif=False,source=source)        
            po = pla.load_pdb()
            pobjs.append(po)
        
        gm = pg.GeometryMaker(pobjs)        
        df_atoms = gm.calculateData()

        code_string += "\ngm = pg.GeometryMaker(pobjs)\n"        
        code_string += "df_atoms = gm.calculateData()\n"
                    
        st.session_state['atoms'] = df_atoms
        st.session_state['code_df'] = code_string

    if len(df_atoms.index) > 0:
        st.write("---")
        st.write("##### View calculated data")                
        with st.expander("Expand atomic dataframe"):
            st.dataframe(df_atoms)
                                                            
        st.write("---")
        st.write("##### Plot spatial data")
        aax_cols = list(df_atoms.columns)
        aiidh1,aiidh2 = 0,0
        try:            
            aiidh1 = aax_cols.index("bfactor")            
            aiidh2 = aax_cols.index("element")
        except:
            pass

        pdbs = list(df_atoms["pdbCode"].unique())
                
        ax_ax1 = "x"        
        ay_ax1 = "y"
        az_ax1 = "z"
        ax_ax2 = "x"        
        ay_ax2 = "y"
        az_ax2 = "z"
                
        cols = st.columns(3)
        with cols[0]:
            pdb = st.selectbox("pdbcode", pdbs,index=0)        
        with cols[1]:
            ah_ax1 = st.selectbox("hue 1",aax_cols,index=aiidh1)        
        with cols[2]:
            ah_ax2 = st.selectbox("hue 2",aax_cols,index=aiidh2)
        if st.button("Calculate atom plot"):
            st.write("Spatial info")
            cols = st.columns(2)
            with cols[0]:                
                fig = px.scatter_3d(df_atoms[df_atoms['pdbCode'] == pdb], x=ax_ax1, y=ay_ax1, z=az_ax1, color=ah_ax1,title="",
                    width=500, height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                st.plotly_chart(fig, use_container_width=False)
            with cols[1]:                
                fig = px.scatter_3d(df_atoms[df_atoms['pdbCode'] == pdb], x=ax_ax2, y=ay_ax2, z=az_ax2, color=ah_ax2,title="",
                    width=500, height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                st.plotly_chart(fig, use_container_width=False)

            code_string2 = "import plotly.express as px\n"
            code_string2 += f"fig = px.scatter_3d(df_atoms, x='x', y='y', z='z',color='{ah_ax1}',title='',\n"
            code_string2 += "    width=500, height=500, opacity=0.5, color_continuous_scale=px.colors.sequential.Viridis))\n"
            code_string2 += "fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))\n"
            code_string2 += "fig.show() #or preferred method, e.g. fig.write_html('path/to/file.html')\n"
            st.session_state['code_df2'] = code_string2

        

with tabCode:
    st.code(st.session_state['code_df'])
    st.code(st.session_state['code_df2'])

st.divider()
st.caption("Crick, F. H. C., & Kendrew, J. C. (1957). X-Ray Analysis and Protein Structure. In Advances in Protein Chemistry (Vol. 12, pp. 133–214). Elsevier. https://doi.org/10.1016/S0065-3233(08)60116-3")

        