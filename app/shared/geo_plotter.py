import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px
from shared import config as cfg



def geo_plot(df_geos):
    cfg.init()
    if df_geos is not None and len(df_geos.index) > 0:
        st.write("### Visualisation")
        ax_cols = list(df_geos.columns)
        ax_colsZ = list(df_geos.columns)
        ax_colsZ.insert(0,"Probability density plot")        
                                                
        
        cols = st.columns([1,2,2,2,1])
        with cols[1]:
            x_ax1 = st.selectbox("x-axis", ax_cols,index=0)
        with cols[2]:
            y_ax1 = st.selectbox("y-axis",ax_cols,index=1)
        with cols[3]:
            z_ax1 = st.selectbox("z-axis (hue)",ax_colsZ,index=3)
                
        if st.button("Calculate geo plot"):                    
            cols = st.columns([1,5,1])
            with cols[1]:
                if z_ax1 == "Probability density plot":
                    fig = px.density_contour(df_geos, x=x_ax1, y=y_ax1, title="",width=500, height=500)
                    fig.update_traces(contours_coloring="fill", contours_showlabels = True)
                else:
                    fig = px.scatter(df_geos, x=x_ax1, y=y_ax1, color=z_ax1,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)                        
                st.plotly_chart(fig, use_container_width=False)
                
def space_plot(df_atoms):
    cfg.init()
    if df_atoms is not None and len(df_atoms.index) > 0:
        st.write("### Visualisation")
        ax_cols = list(["x","y","z"])
        ax_colsZ = list(df_atoms.columns)

        dim = st.radio("dimensions",["2d","3d"],index=0)
                                                                
        cols = st.columns([2,2,2,2,2])
        with cols[0]:
            pdb = st.selectbox("pdb", ["all"] + list(df_atoms["pdb_code"].unique()),index=0)
        with cols[1]:
            x_ax1 = st.selectbox("x-axis", ax_cols,index=0)
        with cols[2]:
            y_ax1 = st.selectbox("y-axis",ax_cols,index=1)
        if dim == "3d":
            with cols[3]:
                z_ax1 = st.selectbox("z-axis",ax_cols,index=2)
            with cols[4]:
                h_ax1 = st.selectbox("hue",ax_colsZ,index=0)
        else:
            with cols[3]:
                h_ax1 = st.selectbox("hue",ax_colsZ,index=0)
                
        df_use = df_atoms
        if pdb != "all":
            df_use = df_atoms[df_atoms['pdb_code'] == pdb]
        if st.button("Calculate geo plot"):                    
            cols = st.columns([1,5,1])
            with cols[1]:                
                if dim == "2d":
                    fig = px.scatter(df_use, x=x_ax1, y=y_ax1, color=h_ax1,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)                        
                    st.plotly_chart(fig, use_container_width=False)
                else:
                    fig = px.scatter_3d(df_use, x=x_ax1, y=y_ax1, z=z_ax1, color=h_ax1,title="",
                        width=500, height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                    fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                    st.plotly_chart(fig, use_container_width=False)

def contact_plot(df_geo):
    cfg.init()
    if df_geo is not None and len(df_geo.index) > 0:
        st.write("### Visualisation")
        geo = df_geo.columns[0]
        rid1 = "rid"
        rid2 = f"rid2_{geo}"
        rid3 = f"rid3_{geo}"
                
        ax_colsZ = list(df_geo.columns)

        dim = "2d"#st.radio("dimensions",["2d","3d"],index=0)
                                                                
        cols = st.columns([1,6,6,1])
        with cols[1]:
            pdb = st.selectbox("pdb", ["all"] + list(df_geo["pdb_code"].unique()),index=0)        
        with cols[2]:
            h_ax1 = st.selectbox("hue",ax_colsZ,index=0)
                
        df_use = df_geo
        if pdb != "all":
            df_use = df_geo[df_geo['pdb_code'] == pdb]
        if st.button("Calculate geo plot"):                    
            cols = st.columns([1,5,1])
            with cols[1]:                
                if dim == "2d":
                    fig = px.scatter(df_use, x=rid1, y=rid2, color=h_ax1,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)                        
                    st.plotly_chart(fig, use_container_width=False)
                else:
                    fig = px.scatter_3d(df_use, x=rid1, y=rid2, z=rid3, color=h_ax1,title="",
                        width=500, height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                    fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                    st.plotly_chart(fig, use_container_width=False)
                        
            