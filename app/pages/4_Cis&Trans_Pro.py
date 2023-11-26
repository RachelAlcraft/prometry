

import streamlit as st
import requests

DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - Proline: cis and trans")

st.caption('''
"when there is uncertainty in lower-resolution structures, the more probable trans-prolines are preferentially chosen in model building, exaggerating their frequency."[1]
''')




st.divider()
st.caption("[1] R. A. Engh and R. Huber, ‘18.3. Structure quality and target parameters’, International Tables for Crystallography, vol. F, pp. 382–392, 2006, doi: http://dx.doi.org/10.1107/97809553602060000695.")
