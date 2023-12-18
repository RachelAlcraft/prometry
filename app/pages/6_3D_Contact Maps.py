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

st.header("Prometry - Contact Maps")
st.caption("""
"NEED A QUOTE
""")
st.write("We can look at all possible pairings of 3 CAs for a more accurate vision of the structural contacts.")

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


    structures = "5nqo"
    geo = "MINDIS|CA:{CA@i}[dis|<10,rid|>1]:{CA@i}[dis|<10,rid|>1]"
    geos = geo
    idx1 = "rid"
    idy1 = f"rid2_{geo}"    
    idz1 = f"rid3_{geo}"
    idhue = geo
                             
    st.write("##### Edit/enter structures and geos")
        
    cols = st.columns([1,1])
    with cols[0]:
        structures = st.text_input("Structures", value=structures,help="pdb or alphafold code")
    with cols[1]:
        geos = st.text_input("List of geometric paramaters",value=geos,help="space delim, 2, 3 or 4 atoms - see help")

    ls_structures = structures.split(" ")
    ls_geos = geos.split(" ")

    df_geos = pd.DataFrame({'A' : []})    
    if 'data' not in st.session_state:
        st.session_state['data'] = df_geos        
    else:
        if st.session_state['pdbs'] != structures or st.session_state['geos'] != geos:
            st.session_state['data'] = df_geos            
            st.session_state['pdbs'] = structures
            st.session_state['geos'] = geos
        else:
            df_geos = st.session_state['data']
                
    st.write("---")
    st.write("##### Calculate dataframe")
    if st.button("Calculate dataframe"):

        code_string += f"ls_structures = {ls_structures}\n"
        code_string += f"ls_geos = {ls_geos}\n"
        
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
        df_geos = gm.calculateGeometry(ls_geos)
        
        code_string += "\ngm = pg.GeometryMaker(pobjs)\n"
        code_string += "df_geos = gm.calculateGeometry(ls_geos)\n"
                    
        st.session_state['data'] = df_geos        
        st.session_state['code_df'] = code_string
                
    if len(df_geos.index) > 0:
        st.write("---")
        st.write("##### View calculated data")
        with st.expander("Expand geometric dataframe"):
            st.dataframe(df_geos)
                                            
        ax_cols = list(df_geos.columns)
        iidx1,iidy1,iidz1,iidhue = 0,0,0,0
        try:
            iidx1 = ax_cols.index(idx1)
            iidy1 = ax_cols.index(idy1)
            iidz1 = ax_cols.index(idz1)
            iidhue = ax_cols.index(idhue)            
        except:
            pass

        

        st.write("---")
        st.write("##### 5) Plot geometric data")
        cols = st.columns(4)
        with cols[0]:
            x_ax1 = st.selectbox("x-axis", ax_cols,index=iidx1)
        with cols[1]:
            y_ax1 = st.selectbox("y-axis",ax_cols,index=iidy1)
        with cols[2]:
            z_ax1 = st.selectbox("z-axis",ax_cols,index=iidz1)        
        with cols[3]:
            z_axhue = st.selectbox("hue",ax_cols,index=iidhue)


        # rename colums
        df_use = df_geos[[x_ax1,y_ax1,z_ax1,z_axhue]]
        print(df_use.columns)
        cols = list(df_use.columns)
        cols[3] = "hue"
        df_use.columns = cols
        
        if st.button("Calculate geo plot"):
            cols = st.columns(1)
            with cols[0]:
                fig = px.scatter_3d(df_use, x=x_ax1, y=y_ax1, z=z_ax1, color="hue",title="", #width=500, 
                height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                st.plotly_chart(fig, use_container_width=False)
            
            
            code_string2 = "import plotly.express as px\n"
            code_string2 += f"fig = px.scatter(df_geos, x='{x_ax1}', y='{y_ax1}', color='{z_ax1}',title="",width=500, height=500, opacity=0.7, color_continuous_scale=px.colors.sequential.Viridis))\n"
            code_string2 += "fig.show() #or preferred method, e.g. fig.write_html('path/to/file.html')"
            st.session_state['code_df2'] = code_string2
                                                                           
            
                        
with tabCode:
    st.code(st.session_state['code_df'])
    st.code(st.session_state['code_df2'])

st.divider()
st.caption("Molkenthin, N., Güven, J. J., Mühle, S., & Mey, A. S. J. S. (2022). What geometrically constrained folding models can tell us about real-world protein contact maps (arXiv:2205.09074). arXiv. http://arxiv.org/abs/2205.09074")
