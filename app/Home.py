import streamlit as st


st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
    )

st.header("PROMETRY")
#tabHi, tabCV, tabAc,tabTeach,TabCom,tabPubs = st.tabs(["Welcome","Career","Academic","Teaching","Community","Publications"])
#with tabHi:
st.write("""                      
         ---  

         Prometry is a python library to calculate the geoemtric parameters of protein structures.                    
         
         This website gives a brief demonstration of some of the ways the prometry can be used.
         As a publicly hosted web application this does not include calculation-time or memory-intense uses such as
          generating and using the data in machine learning applications which the dataframes and contact maps would be suitable for.

         Rather, this application guides you through a variety of uses and is intended to give you ideas and inspiration for your own uses.  

         This site is distributed by continuous depoloyment from the main branch of the github repo
         https://github.com/RachelAlcraft/prometry

         ---  

         **The application is freely available by streamlit at no cost to me or you.**  

         ---  
         
         All the source code for the library and this application is made freely availabe by me to you in the sprit of open science.

         If you make use of anything from this application (dataframe data, plots, python code, scientific ideas...)
         please follow the guidance on the citing page.                     

         ---  
        
        """)

