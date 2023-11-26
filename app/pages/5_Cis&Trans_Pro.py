import streamlit as st
import shared.simple_plotsheet as shared_plot


DATADIR = "app/data/"

st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - Proline: cis and trans")
st.caption('''
"...when there is uncertainty in lower-resolution structures, the more probable trans-prolines are preferentially chosen in model building, exaggerating their frequency."(Engh&Huber, 2006)
''')


st.write("What cis and pro results do we obtain from the ultra-high set? We can use the CA distances as well as pre-omega to explore.")

structures = "1ejg 1gci 1hje 1iua 1pq7 1r6j 1ucs 1us0 1w0n 1x6z 1yk4 2b97 2dsx 2ixt 2ov0 2pve 2qxw 2vb1 2wfi 2ygi 2ygj 3a38 3a39 3bcj 3d43 3mfj 3mi4 3nir 3ui4 3w5h"
#structures += " 3x2m 3x34 4g13 4i8g 4i8h 4lb3 4lb4 4lbr 4lbs 4rek 4ua6 4zm7 5d8v 5gv7 5gv8 5kwm 5mn1 5mnk 5nfm 5nw3 5ome 5wqq 5wqr 5yce 6e6o 6jgj 6kl0 6l27 6mw0 6mw1"
#structures += " 6mw2 6s2m 6tov 6ufa 6zm8 7fez 7kr0 7r2h 7tls 7tlu 7tme 7tmh 7tmi 7vos 8c5n 8gl4"

geos = "CA[aa|20]:CA+1[aa|20] CA-1[aa|20]:CA CA:C:N+1:CA+1 CA-1:C-1:N:CA"

shared_plot.plot_sheet(structures, geos, ("CA:C:N+1:CA+1","CA-1:C-1:N:CA","aa"),("CA[aa|20]:CA+1[aa|20]","CA-1[aa|20]:CA","aa"))





st.divider()
st.caption("Engh, R. A., & Huber, R. (2006). Structure quality and target parameters. In M. G. Rossmann & E. Arnold (Eds.), International Tables for Crystallography: Vol. F (1st ed., pp. 382–392). International Union of Crystallography. https://doi.org/10.1107/97809553602060000695")
