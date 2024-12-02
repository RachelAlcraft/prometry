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

st.header("Prometry - Contact Maps")
st.caption("""
"Contact maps do not only contain the information needed for protein structure prediction, 
but they also are potential tools to describe the fundamentals of protein folding. (Bittrich et al, 2019)"
""")

st.write("""
We can use the distance search for a classic CA-CA contact map, or we could use N:(O@i) for a distance seach on NO. 
Non-standard residues and water can be filtered out by choosing only the standard 20 (aa|20).
""")


strucs = "1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt"
geos = "N:CA:C:N+1 C-1:N:CA:C N:O N:N+1 N:CA:C"

tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:        
        ls_structures, ls_contacts = se.explorer(use_geos="contacts")
        st.write("---")
        df = dm.maker_geos(ls_structures,ls_contacts)
        st.write("---")
        gp.contact_plot(df)
        
with tabCode:
        st.write("not implemented")

st.divider()
st.caption("""
Bittrich, S., Schroeder, M. & Labudde, D. StructureDistiller: 
Structural relevance scoring identifies the most informative entries of a contact map. Sci Rep 9, 18517 (2019). https://doi.org/10.1038/s41598-019-55047-4
""")