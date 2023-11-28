import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px

DATADIR = "app/data/"


def plot_sheet(structuresA,structuresB, geos, id1s,id2s):

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
        
        idx1, idy1,idz1 = id1s
        idx2, idy2,idz2 = id2s        
                                
        st.write("##### Edit/enter structures and geos")
            
        cols = st.columns([1,1,1])
        with cols[0]:
            structuresA = st.text_input("Structures", value=structuresA,help="pdb or alphafold code")
        with cols[1]:
            structuresB = st.text_input("Structures", value=structuresB,help="pdb or alphafold code")
        with cols[2]:
            geos = st.text_input("List of geometric paramaters",value=geos,help="space delim, 2, 3 or 4 atoms - see help")

        ls_structuresA = structuresA.split(" ")
        ls_structuresB = structuresB.split(" ")
        ls_geos = geos.split(" ")

        df_geos = pd.DataFrame({'A' : []})
        df_geosB = pd.DataFrame({'A' : []})
        if 'dataB' not in st.session_state:
            st.session_state['dataB'] = df_geosB
            st.session_state['data'] = df_geos
        else:
            if st.session_state['pdbs'] != structuresA or st.session_state['geos'] != geos:
                st.session_state['data'] = df_geos            
                st.session_state['pdbs'] = structuresA
                st.session_state['pdbsB'] = structuresB
                st.session_state['geos'] = geos
            else:
                df_geos = st.session_state['data']
                df_geosB = st.session_state['dataB']
                    
        st.write("---")        
        if st.button("Calculate dataframe"):

            code_string += f"ls_structuresA = {ls_structuresA}\n"
            code_string += f"ls_structuresB = {ls_structuresB}\n"
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
                    
            for pdb in ls_structuresA:
                try:
                    if "AF-" in pdb:
                        source = "alphafold"
                    else:
                        source = "ebi"
                        pdb = pdb.lower()
                    pla = pl.PdbLoader(pdb,DATADIR,cif=False,source=source)        
                    po = pla.load_pdb()
                    pobjs.append(po)
                except Exception as e:
                    st.error(str(e))            
            gm = pg.GeometryMaker(pobjs)
            df_geos = gm.calculateGeometry(ls_geos)

            pobjsB = []
            for pdb in ls_structuresB:
                try:
                    if "AF-" in pdb:
                        source = "alphafold"
                    else:
                        source = "ebi"
                        pdb = pdb.lower()
                    pla = pl.PdbLoader(pdb,DATADIR,cif=False,source=source)        
                    po = pla.load_pdb()
                    pobjsB.append(po)
                except Exception as e:
                    st.error(str(e))            
            gm = pg.GeometryMaker(pobjsB)
            df_geosB = gm.calculateGeometry(ls_geos)
            
            code_string += "\ngm = pg.GeometryMaker(pobjs)\n"
            code_string += "df_geos = gm.calculateGeometry(ls_geos)\n"
                        
            st.session_state['data'] = df_geos        
            st.session_state['dataB'] = df_geosB
            st.session_state['code_df'] = code_string
                    
        if len(df_geos.index) > 0:
            st.write("---")
            st.write("##### View calculated data")
            with st.expander("Expand geometric dataframe"):
                st.dataframe(df_geos)
                                                
            ax_cols = list(df_geos.columns)
            iidx1,iidy1,iidz1,iidx2,iidy2,iidz2 = 0,0,0,0,0,0
            try:
                iidx1 = ax_cols.index(idx1)
                iidy1 = ax_cols.index(idy1)
                iidz1 = ax_cols.index(idz1)
                iidx2 = ax_cols.index(idx2)
                iidy2 = ax_cols.index(idy2)
                iidz2 = ax_cols.index(idz2)
            except:
                pass
            
            st.write("---")
            st.write("##### Plot geometric data")
            cols = st.columns(6)
            with cols[0]:
                x_ax1 = st.selectbox("x-axis 1", ax_cols,index=iidx1)
            with cols[1]:
                y_ax1 = st.selectbox("y-axis 1",ax_cols,index=iidy1)
            with cols[2]:
                z_ax1 = st.selectbox("z-axis (hue) 1",ax_cols,index=iidz1)
            with cols[3]:
                x_ax2 = st.selectbox("x-axis 2", ax_cols,index=iidx2)
            with cols[4]:
                y_ax2 = st.selectbox("y-axis 2",ax_cols,index=iidy2)
            with cols[5]:
                z_ax2 = st.selectbox("z-axis (hue) 2",ax_cols,index=iidz2)
            
            if st.button("Calculate geo plot"):
                cols = st.columns(2)
                with cols[0]:
                    fig = px.scatter(df_geos, x=x_ax1, y=y_ax1, color=z_ax1,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)
                    st.plotly_chart(fig, use_container_width=False)
                    figB = px.scatter(df_geosB, x=x_ax1, y=y_ax1, color=z_ax1,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)
                    st.plotly_chart(figB, use_container_width=False)
                with cols[1]:
                    fig = px.scatter(df_geos, x=x_ax2, y=y_ax2, color=z_ax2,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)
                    st.plotly_chart(fig, use_container_width=False)
                    figB = px.scatter(df_geosB, x=x_ax2, y=y_ax2, color=z_ax2,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)
                    st.plotly_chart(figB, use_container_width=False)
                
                code_string2 = "import plotly.express as px\n"
                code_string2 += "# Choose the dataframe you want to look at, df_geos or df_geosB\n"
                code_string2 += f"fig = px.scatter(df_geos, x='{x_ax1}', y='{y_ax1}', color='{z_ax1}',title="",width=500, height=500, opacity=0.7, color_continuous_scale=px.colors.sequential.Viridis))\n"
                code_string2 += "fig.show() #or preferred method, e.g. fig.write_html('path/to/file.html')"
                st.session_state['code_df2'] = code_string2
                                                                                                                        
    with tabCode:
        st.code(st.session_state['code_df'])
        st.code(st.session_state['code_df2'])

    