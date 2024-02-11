import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from shared import config as cfg
import numpy as np



def geo_plot(df_geos):
    cfg.init()
    if df_geos is not None:        
        if len(df_geos.index) > 0:
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
                        print("HERE")
                        fig = px.scatter(df_geos, x=x_ax1, y=y_ax1, color=z_ax1,title="",width=500, height=500, opacity=0.7,color_continuous_scale=px.colors.sequential.Viridis)
                    st.plotly_chart(fig, use_container_width=False)     
                
def geo_plot_ramachandran(df_geos):
    from PIL import Image    
    img1 = Image.open("app/static/rama_all.png")
    img2 = Image.open("app/static/rama_pro.png")
    img3 = Image.open("app/static/rama_gly.png")
    if df_geos is not None:        
        if len(df_geos.index) > 0:
            st.write("### Overlay Ramachandran")            
            ax_colsZ = list(df_geos.columns)[2:7] + ["bf_C-1:N:CA:C","bf_N:CA:C:N+1"]
            x_ax1 = "C-1:N:CA:C"
            y_ax1 = "N:CA:C:N+1"
            cols = st.columns([1,2,5])
            with cols[0]:
                st.write("hue:")
            with cols[1]:
                z_ax1 = st.selectbox("z-axis (hue)",ax_colsZ,index=0,label_visibility="collapsed")
                    
            if st.button("Calculate geo plot"):                    
                cols = st.columns([1,7,7,7,1])                                
                plots_obj = []
                plots_obj.append((1,"exc PRO&GLY",img1,df_geos[df_geos.aa != "PRO"][df_geos.aa != "GLY"]))
                plots_obj.append((2,", PRO",img2,df_geos[df_geos.aa == "PRO"]))
                plots_obj.append((3,", GLY",img3,df_geos[df_geos.aa == "GLY"]))
                for col,aa,img,df in plots_obj:                          
                    with cols[col]:                        
                        fig = px.scatter(df, x=x_ax1, y=y_ax1, color=z_ax1,title="", opacity=0.6,color_continuous_scale="temps")
                        fig.update_layout(title=f"Ramachandran {aa} ({len(df.index)})",autosize = False,
                            xaxis = dict(zeroline = False, domain = [0,0.85],showgrid = False,range=[-180,180]),
                            yaxis = dict(zeroline = False, domain = [0,0.85],showgrid = False,range=[-180,180]),                        
                            height = 500, width = 500,  
                            bargap = 0,  hovermode = 'closest',  showlegend = True
                        )  
                        fig.add_layout_image(dict(source=img, xref="x", yref="y", x=0,y=180, xanchor="center", sizex=360, sizey=360, sizing="stretch", opacity=0.35, layer="below"))                                                                                       
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
                else:
                    fig = px.scatter_3d(df_use, x=rid1, y=rid2, z=rid3, color=h_ax1,title="",
                        width=500, height=500, opacity=0.5,color_continuous_scale=px.colors.sequential.Viridis)
                    fig.update_traces(marker=dict(size=5,line=dict(width=0,color='silver')),selector=dict(mode='markers'))
                
                fig.update_layout(title=f"Contact map",autosize = False,
                        xaxis = dict(zeroline = False, domain = [0,0.85],showgrid = False,range=[-180,180]),
                        yaxis = dict(zeroline = False, domain = [0,0.85],showgrid = False,range=[-180,180]),                        
                        height = 800, width = 800,  
                        bargap = 0,  hovermode = 'closest',  showlegend = True
                    ) 
                st.plotly_chart(fig, use_container_width=False)

# taken from 18.3. STRUCTURE QUALITY AND TARGET PARAMETERS
# Table 18.3.2.3. Bond lengths (  ̊ A) and angles (°) of peptide backbone fragments

EH_2006_median = {}
EH_2006_median["N:CA"]=(1.459,1.468,1.456)
EH_2006_median["CA:C"]=(1.525,1.524,1.514)
EH_2006_median["C:O"]=(1.229,1.228,1.232)
EH_2006_median["C:N+1"]=(1.336,1.338,1.326)

EH_2006_median["N:CA:C"]= (111.0,112.1,113.1)
EH_2006_median["CA:C:N+1"]= (117.2,117.1,116.2)
EH_2006_median["CA:C:O"]= (120.1,120.2,120.6)
EH_2006_median["O:C:N+1"]= (122.7,121.1,123.2)
EH_2006_median["C-1:N:CA"]= (121.7,122,122.3)




def val_plot(df_geos,geo):
    cfg.init()
    if df_geos is not None:        
        if len(df_geos.index) > 0:
            st.write("### Validation")

            val_lines = 0,0,0
            if geo in EH_2006_median:
                val_lines = EH_2006_median[geo]
                                                                                                    
            if st.button("Calculate geo plot"):                    
                cols = st.columns([1,5,5,5,1])
                pdbs = set(df_geos["pdb_code"])
                if len(pdbs) > 1:
                    # first summarise
                    plots_obj = []
                    plots_obj.append((1,"exc PRO&GLY",val_lines[0],df_geos[df_geos.aa != "PRO"][df_geos.aa != "GLY"]))
                    plots_obj.append((2,"PRO",val_lines[1],df_geos[df_geos.aa == "PRO"]))
                    plots_obj.append((3,"GLY",val_lines[2],df_geos[df_geos.aa == "GLY"]))
                    for col,aa,val_line,df in plots_obj:                
                            with cols[col]:                
                                fig = px.histogram(df, 
                                                    x=geo,
                                                    title=f"Distribution of {geo}, {aa} ({len(df.index)})",
                                                    #marginal="box", # or violin, rug
                                                    color="pdb_code",opacity=0.85)
                                if val_line != 0:                         
                                    fig.add_vline(x=val_line, line_dash = 'dash', line_color = 'crimson', annotation_text=f"E&H",annotation_textangle=55,annotation_position="top")
                                
                                fig.update_annotations(font=dict(color="black"))
                                fig.update_traces(marker=dict(line=dict(width=0.2,color='white')))                                                         
                                st.plotly_chart(fig, use_container_width=True)

                
                for pdb in pdbs:            
                    df_geos_pdb = df_geos[df_geos.pdb_code == pdb]                
                    plots_obj = []
                    plots_obj.append((1,"exc PRO&GLY",val_lines[0],df_geos_pdb[df_geos_pdb.aa != "PRO"][df_geos_pdb.aa != "GLY"]))
                    plots_obj.append((2,"PRO",val_lines[1],df_geos_pdb[df_geos_pdb.aa == "PRO"]))
                    plots_obj.append((3,"GLY",val_lines[2],df_geos_pdb[df_geos_pdb.aa == "GLY"]))
                    for col,aa,val_line,df in plots_obj:                
                        with cols[col]:                
                            fig = px.histogram(df, 
                                                x=geo,
                                                title=f"Distribution of {geo}, {aa}<br>in {pdb} ({len(df.index)})",                                            
                                                color_discrete_sequence=['CornflowerBlue'],opacity=1)
                            fig.add_vline(x=np.median(df[geo]), line_dash = 'dash', line_color = 'Gold', annotation_text="median",annotation_textangle=55,annotation_position="top")
                            fig.add_vline(x=np.quantile(df[geo],0.25), line_dash = 'dash', line_color = 'Gold', annotation_text="25%",annotation_textangle=55,annotation_position="top")
                            fig.add_vline(x=np.quantile(df[geo],0.75), line_dash = 'dash', line_color = 'Gold', annotation_text="75%",annotation_textangle=55,annotation_position="top")
                            if val_line != 0:                         
                                fig.add_vline(x=val_line, line_dash = 'dash', line_color = 'crimson', annotation_text=f"E&H",annotation_textangle=55,annotation_position="top")

                            #fig.update_annotations(font=dict(family="sans serif", size=14, color="navy"))
                            fig.update_annotations(font=dict(color="black"))
                            fig.update_traces(marker=dict(line=dict(width=0.2,color='white')))                                 
                            #if len(geo.split(":")) == 2:
                            #    fig.update_traces(xbins=dict(size=0.0025))
                            #else:
                            #    fig.update_traces(xbins=dict(size=0.5))
                            st.plotly_chart(fig, use_container_width=True)

                                
                    