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

st.header("Prometry - Geometry playsheet")
st.caption("""
"One approach is using protein contact maps to better understand proteins' properties."(Molkenthin et al, 2022)
""")

st.write("""
We can use the distance search for a classic CA-CA contact map, or we could use N:(O@i) for a distance seach on NO. 
Non-standard residues and water can be filtered out by choosing only the standard 20 (aa|20).
""")


strucs = "1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt"
geos = "N:CA:C:N+1 C-1:N:CA:C N:O N:N+1 N:CA:C"

tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:        
        ls_structures, ls_geos = se.explorer(use_geos="contacts")
        st.write("---")
        df = dm.maker_geos(ls_structures,ls_geos)
        st.write("---")
        gp.contact_plot(df)
        st.write("---")

with tabCode:
        st.write("not implemented")

st.divider()
st.caption("""
Molkenthin, N., Güven, J. J., Mühle, S., & Mey, A. S. J. S. (2022). 
What geometrically constrained folding models can tell us about real-world protein contact maps (arXiv:2205.09074). arXiv. http://arxiv.org/abs/2205.09074
""")