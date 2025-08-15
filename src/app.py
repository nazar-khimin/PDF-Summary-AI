import streamlit as st
from dotenv import load_dotenv
from pdf_loader import load_pdf
from openai_clients import get_gpt_4o_mini_llm, get_gpt5_mini_llm
from summarizer import summarize_pdf

load_dotenv()
st.set_page_config(page_title="📄 PDF Summarizer", layout="centered")
st.title("📄 PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    docs = load_pdf(uploaded_file)
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_pdf(docs)
                st.subheader("Summary:")
                st.markdown(summary)
            except Exception as e:
                st.error(f"❌ Error: {e}")