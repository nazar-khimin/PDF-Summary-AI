import streamlit as st
from dotenv import load_dotenv
import tempfile
import os

from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

st.title("📄 PDF Summarizer")

# Modular PDF loading and splitting
def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name

    loader = PyMuPDF4LLMLoader(
        tmp_path,
        mode='page',
        extract_images=True,
        images_parser=LLMImageBlobParser(
            model=ChatOpenAI(model="gpt-5-mini", max_tokens=1024)
        ),
        table_strategy="lines_strict"
    )

    documents = loader.load()

    # Clean up temp file after loading
    os.remove(tmp_path)

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="o200k_base",
        chunk_size=1800,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_documents(documents)

# Summarization logic
def summarize_documents(docs, llm, chain_type="stuff"):
    chain = load_summarize_chain(llm, chain_type=chain_type)
    return chain.invoke({"input_documents": docs})["output_text"]

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    docs = load_pdf(uploaded_file)

    llm = ChatOpenAI(temperature=0, model_name="gpt-5-mini")

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_documents(docs, llm)
                st.subheader("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"❌ Error: {e}")