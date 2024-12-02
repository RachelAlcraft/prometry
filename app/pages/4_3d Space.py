import streamlit as st
import shared.simple_plotsheet as shared_plot
import shared.structure_explorer as se
import shared.dataframe_maker as dm
import shared.geo_plotter as gp

DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - atoms in 3d space")
st.caption(''' 
"Here we shall use the term 'protein structure' in an entirely different sense... Whereas Anfinsen and Redfield have concerned themselves 
with the amino acid sequence and topological interconnections of the polypeptide chains, we shall consider mainly the geometrical 
aspects - the arrangement of the atoms in space."(Crick&Kendrew, 1957)
''')

st.write("""
The plDDT (bfactor) is interesting for AlphaFold structures, showing a characteristic predictive format of a high plDDT
core - a region where there are generally solved structures - with hightly uncertain regions at the edges.
""")


strucs = "1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt"
geos = "N:CA:C:N+1 C-1:N:CA:C N:O N:N+1 N:CA:C"

tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:        
        ls_structures, ls_geos = se.explorer(use_geos="no")
        st.write("---")
        df = dm.maker_atoms(ls_structures)
        st.write("---")
        gp.space_plot(df)
        
with tabCode:
        st.write("not implemented")

st.divider()
st.caption("Crick, F. H. C., & Kendrew, J. C. (1957). X-Ray Analysis and Protein Structure. In Advances in Protein Chemistry (Vol. 12, pp. 133–214). Elsevier. https://doi.org/10.1016/S0065-3233(08)60116-3")