
import streamlit as st

DATADIR = "app/data/"

def init():
    # All key initilisation
    if 'df_geos' not in st.session_state:
        st.session_state['df_geos'] = None
    if 'df_atoms' not in st.session_state:
        st.session_state['df_atoms'] = None
    if "ls_structures" not in st.session_state:
        st.session_state["ls_structures"] = ["AF-P04637-F1-model_v4","1YCS"]
    if "ls_geos" not in st.session_state:
        st.session_state["ls_geos"] = ["C-1:N:CA:C","N:CA:C:N+1","N:O","N:N+1","N:CA:C"]