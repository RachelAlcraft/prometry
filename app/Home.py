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
         
         
         Prometry is a python library to calculate the geoemtric parameters of protein structures.                    
         
         This website gives a brief demonstration of some of the ways that prometry can be used.
         As a publicly hosted web application this does not include time and memory-intense uses such as
          generating and using the data in machine learning applications, although the dataframes and contact maps would be very suitable for such applications.

         Rather, this application guides you through the assorted variety of uses. It is intended to spark links and inspiration for your own ideas.
    """)
    
st.write("""                      
         ---           

         **The application is freely available by streamlit at no cost to me or you.**  

         ---  
         
         All the source code for the library and this application is made freely available by me to you in the sprit of open science.

         If you make use of anything from this application (dataframe data, plots, python code, scientific ideas...)
         please follow the guidance on the [Citing](https://prometry.streamlit.app/Citing) page.                     

         ---  

         This application has been developed by [Rachel Alcraft](mailto:rachelalcraft@gmail.com) as an offshoot of a PhD at Birkbeck, University of London (C) 2023

         ---  

         This site is distributed by continuous deployment from the main branch of the github repo
         https://github.com/RachelAlcraft/prometry
         
         ---  
                 
        """)

