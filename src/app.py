import streamlit as st
from dotenv import load_dotenv
from pdf_loader import load_pdf
from summarizer import summarize_pdf

load_dotenv()
st.set_page_config(page_title="📄 PDF Summarizer", layout="centered")
st.title("📄 PDF Summarizer")

uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_pdf:
    pdf = load_pdf(uploaded_pdf)
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_pdf(pdf)
                st.subheader("Summary:")
                st.markdown(summary)
            except Exception as e:
                st.error(f"❌ Error: {e}")