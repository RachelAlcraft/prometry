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
st.caption('''
"Proteins are essential to life, and understanding their structure can facilitate a mechanistic understanding of their function."(Jumper et al, 2021)
''')
st.write("Edit the structures and the geometric definitions to find any geometric information for your chosen structures. The further pages offer guidance.")
strucs = "1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt"
geos = "N:CA:C:N+1 C-1:N:CA:C N:O N:N+1 N:CA:C"

tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:        
        ls_structures, ls_geos = se.explorer()        
        st.write("---")
        df = dm.maker_geos(ls_structures, ls_geos)                        
        st.write("---")
        gp.geo_plot(df)
        
with tabCode:
        st.write("not implemented")

st.divider()
st.caption("Jumper, J., Evans, R., Pritzel, A., Green, T., Figurnov, M., Ronneberger, O., Tunyasuvunakool, K., Bates, R., Žídek, A., Potapenko, A., Bridgland, A., Meyer, C., Kohl, S. A. A., Ballard, A. J., Cowie, A., Romera-Paredes, B., Nikolov, S., Jain, R., Adler, J.,Hassabis, D. (2021). Highly accurate protein structure prediction with AlphaFold. Nature, 596(7873), 583–589. https://doi.org/10.1038/s41586-021-03819-2")
