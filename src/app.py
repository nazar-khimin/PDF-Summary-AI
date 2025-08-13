import streamlit as st

from pdf_manager import parser_pdf_file

st.set_page_config(page_title="PDF Summary AI", page_icon="random")


uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    df = parser_pdf_file(uploaded_file)