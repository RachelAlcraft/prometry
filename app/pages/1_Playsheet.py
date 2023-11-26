import streamlit as st
import shared.simple_plotsheet as shared_plot

DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - example and playsheet")
st.caption('''
"Here we shall use the term 'protein structure' in an entirely different sense - indeed, there is very little common ground between the two articles. 
Whereas Anfinsen and Redfield have concerned themselves with the amino acid sequence and topological interconnections of the polypeptide chains, 
we shall consider mainly the geometrical aspects - the arrangement of the atoms in space."(Crick&Kendrew, 1957)
''')
st.write("Edit the structures and the geometric definitions to find any geometric information for your chosen structures. The further pages offer guidance.")
strucs = "1crn 1ejg 3u7t 2fd7 1cbn 1cnr 3nir 1ab1 2fd9 1jxy 1jxu 1jxx 1jxw 1jxt"
geos = "N:CA:C:N+1 C-1:N:CA:C N:O N:N+1 N:CA:C"
shared_plot.plot_sheet(strucs, geos, ("C-1:N:CA:C","N:CA:C:N+1","aa"),("N:CA:C:N+1","N:O","N:CA:C"))


st.divider()
st.caption("Crick, F. H. C., & Kendrew, J. C. (1957). X-Ray Analysis and Protein Structure. In Advances in Protein Chemistry (Vol. 12, pp. 133–214). Elsevier. https://doi.org/10.1016/S0065-3233(08)60116-3")
