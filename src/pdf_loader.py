import os
import tempfile
from contextlib import contextmanager
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf
from openai_clients import get_gpt_4o_mini_llm

MAX_PAGES_LIMIT = 100


@contextmanager
def temp_pdf_file(uploaded_file):
    """Write uploaded file to a temp .pdf and auto-cleanup."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name
        tmp.close()
        yield tmp_path
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def load_pdf(uploaded_file):
    with temp_pdf_file(uploaded_file) as pdf_path:
        validate_pdf_pages(pdf_path, MAX_PAGES_LIMIT)
        docs = PyMuPDF4LLMLoader(
            pdf_path,
            mode="page",
            extract_images=True,
            images_parser=LLMImageBlobParser(model=get_gpt_4o_mini_llm()),
            table_strategy="lines_strict"
        ).load()

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "]
    )
    return splitter.split_documents(docs)


def validate_pdf_pages(pdf_path: str, max_pages: int) -> None:
    with pymupdf.open(pdf_path) as doc:
        if doc.page_count > max_pages:
            raise ValueError(f"PDF has {doc.page_count} pages (limit {max_pages}).")
