from io import BytesIO
from typing import List

from pdf_processor import PDFProcessor
from summarizer import summarize_chunks

def load_pdf(uploaded_file: BytesIO, max_pages: int = 100) -> PDFProcessor:
    processor = PDFProcessor(uploaded_file)
    processor.extract()
    processor.check_page_limit(max_pages=max_pages)
    return processor

def generate_summary(chunks: List[str]) -> str:
    summaries = summarize_chunks(chunks)
    return "\n\n".join(summaries)