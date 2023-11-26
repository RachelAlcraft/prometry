import streamlit as st
from PIL import Image


st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
    )

st.header("PROMETRY")
st.write("#### A library to calculate geometric parameters of protein structures and perform criteria search.")


cols = st.columns([1,3])
with cols[0]:
    image = Image.open('app/static/plot.png')
    st.image(image, caption='BRCA1 AlphaFold structure plotted in 3d')
with cols[1]:
    st.write("""                               
         
         
         Prometry is a python library to calculate the geometric parameters of protein structures.                    
         
         This website gives a brief demonstration of some of the ways that prometry can be used.
         As a publicly hosted web application this does not include time and memory-intense uses such as
          generating and using the data in machine learning applications, although the dataframes and contact maps would be very suitable for such applications.

         Rather, this application guides you through the assorted variety of uses. It is intended to spark links and inspiration for your own ideas.

         All the code for the website is given on a "code" tab on each page so you can replicate all of the results here in python yourself easily and build on it.  
         
         You can also make use of this website directly to create all your data - all the plots and dataframes are downloadable.
    """)
    
st.write("""                      
         
         Prometry has a defined geoemtric-search language described in the [help pages](https://prometry.streamlit.app/Help). 
         It can find distances, angles or dihedrals by describing 2,3 or 4 atoms respectively using the standard atom names for proteins.
         The 20 standard amino acids and their atoms can be [viewed here](https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/formuleAA/).

         Additionally criteria can be described to expand or decrease the search space such as distance criteria and amioa acid restrictions. 
         This means the library can create dataframes for uses as diverse as contact maps, nearest neighbours, possible hydrogen bonds or a simple correlation such as the Ramachandran plot.

         ---           

         **The application is made freely available by streamlit at no cost to me or you.**  

         ---  
         
         All the source code for the library and this application is made freely available by me to you in the spirit of open science.

         If you make use of anything from this application (dataframe data, plots, python code, scientific ideas...)
         please follow the guidance on the [Citing](https://prometry.streamlit.app/Citing) page.                     
                 
         Please raise any requests or problems as a [github issue](https://github.com/RachelAlcraft/prometry/issues)
                     
         ---  
                 
        """)

#st.caption(" This site is distributed by continuous deployment from the main branch of the [github repo](https://github.com/RachelAlcraft/prometry)")
st.caption("This application has been developed by [Rachel Alcraft](mailto:rachelalcraft@gmail.com) as an offshoot of a PhD at Birkbeck, University of London &copy; Rachel Alcraft (2023). Supervisor Dr. Mark A. Williams.")
