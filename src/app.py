import streamlit as st
from io import BytesIO

from pdf_processor import PDFProcessor

st.set_page_config(page_title="PDF Summary AI", page_icon="📄")
st.title("📄 PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF (max 100 pages)", type=["pdf"])

if uploaded_file:
    try:
        pdf_processor = PDFProcessor(BytesIO(uploaded_file.read()))

        with st.spinner("Parsing PDF..."):
            pdf_processor.extract()
            pdf_processor.check_page_limit(max_pages=100)
            chunks = pdf_processor.chunk_text(max_chars=3000)

    except ValueError as ve:
        st.error(str(ve))
    except Exception as e:
        st.error(f"Unexpected error: {e}")