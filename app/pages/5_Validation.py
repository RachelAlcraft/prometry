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

st.header("Validation - Compare Geometry against Engh&Huber")
st.caption('''
“...protein structures are generally solved not to build a statistically optimized protein database, 
but to discover biophysical functional mechanisms.” (Engh & Huber, 2006)."
''')

st.write("""

""")


strucs = "1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt"
geos = "N:CA:C:N+1 C-1:N:CA:C N:O N:N+1 N:CA:C"

tabDemo,tabCode = st.tabs(["demo","code"])

with tabDemo:        
        ls_structures, ls_geos = se.explorer(use_geos="validation")
        st.write("---")
        df,df_extra = dm.maker_geos(ls_structures, ls_geos,extra_underlying=True)
        st.write("---")
        if ls_geos == ["C-1:N:CA:C","N:CA:C:N+1"]:
                gp.geo_plot_ramachandran(df)
                #gp.geo_plot_underlying(df,df_extra)
        else:
                gp.val_plot(df,ls_geos[0])
        st.write("---")

with tabCode:
        st.write("not implemented")

st.divider()
st.write("Plots underlayed with ideal Ramachandran from Lovell, 2003")
st.caption("Engh, R. A., & Huber, R. (2006). 18.3. Structure quality and target parameters. International Tables for Crystallography, F, 382–392. http://dx.doi.org/10.1107/97809553602060000695")
st.caption("Lovell, S. C., Davis, I. W., Arendall, W. B., De Bakker, P. I. W., Word, J. M., Prisant, M. G., Richardson, J. S., & Richardson, D. C. (2003). Structure validation by Cα geometry: ϕ,ψ and Cβ deviation. Proteins: Structure, Function, and Bioinformatics, 50(3), 437–450. https://doi.org/10.1002/prot.10286")
