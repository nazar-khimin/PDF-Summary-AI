import tempfile
import pymupdf

from typing import Iterator
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_core.documents import Document
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from openai_clients import get_gpt_4_nano_llm

MAX_PAGES_LIMIT = 100


def save_pdf_file(uploaded_file) -> str:
    """Save uploaded file to a temp .pdf and return path."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.write(uploaded_file.getbuffer())
    tmp_path = tmp.name
    tmp.close()
    return tmp_path

def load_pdf(uploaded_file) -> Iterator[Document]:
    pdf_path = save_pdf_file(uploaded_file)
    validate_pdf_pages(pdf_path, MAX_PAGES_LIMIT)
    loader = PyMuPDF4LLMLoader(
        pdf_path,
        mode="page",
        extract_images=True,
        images_parser=LLMImageBlobParser(model=get_gpt_4_nano_llm()),
        table_strategy="lines_strict"
    )

    return loader.lazy_load()


def validate_pdf_pages(pdf_path: str, max_pages: int) -> None:
    with pymupdf.open(pdf_path) as doc:
        if doc.page_count > max_pages:
            raise ValueError(f"PDF has {doc.page_count} pages (limit {max_pages}).")
