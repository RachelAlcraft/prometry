import streamlit as st
import shared.simple_plotsheet as shared_plot


st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
)

st.header("Prometry - Geometry as a function of resolution")
st.caption('''
"The main-chain bond lengths and bond angles of protein structures are analysed as a function of resolution. 
Neither the means nor standard deviations of these parameters show any correlation with resolution over the resolution range investigated. 
This is as might be expected as bond lengths and bond angles are likely to be heavily influenced by the geometrical restraints applied during structure refinement."
(Laskowski et al, 1993)
''')

st.write("Ultra-high resolution structures may give new insights into geometric parameters. This set are the protein monomers better than or equal to 0.8Å")

structures = "1ejg 1gci 1hje 1iua 1pq7 1r6j 1ucs 1us0 1w0n 1x6z 1yk4 2b97 2dsx 2ixt 2ov0 2pve 2qxw 2vb1 2wfi 2ygi 2ygj 3a38 3a39 3bcj 3d43 3mfj 3mi4 3nir 3ui4 3w5h"
structures += " 3x2m 3x34 4g13 4i8g 4i8h 4lb3 4lb4 4lbr 4lbs 4rek 4ua6 4zm7 5d8v 5gv7 5gv8 5kwm 5mn1 5mnk 5nfm 5nw3 5ome 5wqq 5wqr 5yce 6e6o 6jgj 6kl0 6l27 6mw0 6mw1"
structures += " 6mw2 6s2m 6tov 6ufa 6zm8 7fez 7kr0 7r2h 7tls 7tlu 7tme 7tmh 7tmi 7vos 8c5n 8gl4"

shared_plot.plot_sheet(structures, "N:CA CA:C CA-1:CA CA:CA+1 N:CA:C:N+1 C-1:N:CA:C C:O", ("CA:C","N:CA","resolution"),("C-1:N:CA:C","N:CA:C:N+1","resolution"))



st.divider()
st.caption("Laskowski, R. A., Moss, D. S., & Thornton, J. M. (1993). Main-chain Bond Lengths and Bond Angles in Protein Structures. Journal of Molecular Biology, 231(4), 1049–1067. https://doi.org/10.1006/jmbi.1993.1351")


