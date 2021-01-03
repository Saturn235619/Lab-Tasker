import pandas as pd
import streamlit as st
import base64

def get_uploaded_file():    
    uploaded_file = st.file_uploader(
                "Please Upload the file containing the data you need plotted",
                type="csv")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        st.table(dataframe)
    
    return dataframe

def get_download_links(image):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    if image is not None:
        image = base64.b64encode(image).decode()
        href = f'''<a href="data:image/png;base64,{image}" download="plot.svg">Download Image</a>'''
        return href
    else:
        pass
