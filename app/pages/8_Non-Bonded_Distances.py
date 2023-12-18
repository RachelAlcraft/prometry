import streamlit as st
import shared.simple_plotsheet as shared_plot


DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - Non-bonded distances")
st.caption('''
"... the vast numbers of hydrogen bonds have a major influence on protein folding."(McDonald&Thornton, 1994)
''')
st.write("We can find all the possible pairings that fulfill a hydrogen bonding distance, varying to extremes if we wish.")


structures = "4rek"
geo = "N:(O@i)[dis|2.2><3.1,rid|>2]"
geos = geo

shared_plot.plot_sheet(structures, geos,("rid",geo,f"info_{geo}"),(geo,f"bf_{geo}","aa"))





st.divider()
st.caption("McDonald, I. K., & Thornton, J. M. (1994). Satisfying Hydrogen Bonding Potential in Proteins. Journal of Molecular Biology, 238(5), 777–793. https://doi.org/10.1006/jmbi.1994.1334")


