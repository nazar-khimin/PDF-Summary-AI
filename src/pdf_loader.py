import tempfile
from typing import Iterator

import pymupdf

MAX_PAGES_LIMIT = 100


def _save_pdf_file(file) -> str:
    """Save uploaded file to a temp .pdf and return path."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.write(file.getbuffer())
    tmp_path = tmp.name
    tmp.close()
    return tmp_path


def load_pdf(file) -> str:
    pdf_path = _save_pdf_file(file)
    validate_pdf_pages(pdf_path, MAX_PAGES_LIMIT)

    return pdf_path


def validate_pdf_pages(pdf_path: str, max_pages: int) -> None:
    with pymupdf.open(pdf_path) as doc:
        if doc.page_count > max_pages:
            raise ValueError(f"PDF has {doc.page_count} pages (limit {max_pages}).")
