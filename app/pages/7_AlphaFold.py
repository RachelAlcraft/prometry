import streamlit as st
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
import pandas as pd
import plotly.express as px
import shared.simple_plotsheet_2_strucs as plot2


DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - AlphaFold structures")
st.caption('''
"Proteins are essential to life, and understanding their structure can facilitate a mechanistic understanding of their function."(Jumper et al, 2021)
''')
st.caption('''
"As AlphaFold predictions can differ substantially from corresponding experimental models, 
straightforward methods to estimate coordinate uncertainties of these predictions would be useful."(Terwilliger et al, 2022)
''')
st.write("Exploration has shown that nearest plots can show impossible clashes in AlphaFold structures, such as this clash in MAST4 between a proline and a cysteine.")

af_structure = "AF-O15021-F1-model_v4"
structures = "2W7R"
geos = "CA:{CA&1}"
id1s = ("CA:{CA&1}","info_CA:{CA&1}","bf_CA:{CA&1}")
id2s = ("rid","CA:{CA&1}","aa")

plot2.plot_sheet(af_structure,structures, geos, id1s,id2s)

st.divider()
st.caption("Jumper, J., Evans, R., Pritzel, A., Green, T., Figurnov, M., Ronneberger, O., Tunyasuvunakool, K., Bates, R., Žídek, A., Potapenko, A., Bridgland, A., Meyer, C., Kohl, S. A. A., Ballard, A. J., Cowie, A., Romera-Paredes, B., Nikolov, S., Jain, R., Adler, J.,Hassabis, D. (2021). Highly accurate protein structure prediction with AlphaFold. Nature, 596(7873), 583–589. https://doi.org/10.1038/s41586-021-03819-2")
st.caption("Terwilliger, T. C., Liebschner, D., Croll, T. I., Williams, C. J., McCoy, A. J., Poon, B. K., Afonine, P. V., Oeffner, R. D., Richardson, J. S., Read, R. J., & Adams, P. D. (2022). AlphaFold predictions are valuable hypotheses, and accelerate but do not replace experimental structure determination [Preprint]. Biochemistry. https://doi.org/10.1101/2022.11.21.517405")





