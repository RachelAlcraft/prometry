
import streamlit as st


DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - Engh&Huber parameter analysis")
st.caption('''
"...protein structures are generally solved not to build a statistically optimized protein database, but to discover biophysical functional mechanisms."(Engh&Huber, 2006))
''')
st.write("Individual structures are not solved with the solution of future structures in mind")
st.divider()



st.divider()
st.caption("Engh, R. A., & Huber, R. (2006). Structure quality and target parameters. In M. G. Rossmann & E. Arnold (Eds.), International Tables for Crystallography: Vol. F (1st ed., pp. 382–392). International Union of Crystallography. https://doi.org/10.1107/97809553602060000695")
