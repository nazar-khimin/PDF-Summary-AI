from typing import List, Dict, Any, TypedDict
from io import BytesIO
import pdfplumber


# --- Typed Structures ---

class PDFPage(TypedDict):
    page_num: str
    text: str
    char_count: str


class PDFContent(TypedDict, total=False):
    text: List[PDFPage]
    tables: Any
    images: Any


# --- Processor Class ---

class PDFProcessor:
    def __init__(self, file: BytesIO):
        self.file = file
        self.content: PDFContent = {}

    def extract(self) -> None:
        with pdfplumber.open(self.file) as pdf:
            self.content["text"] = self._extract_text(pdf)
            # self.content["tables"] = self._extract_tables(pdf)
            # self.content["images"] = self._extract_images(pdf)

    @staticmethod
    def _extract_text(pdf: pdfplumber.PDF) -> List[PDFPage]:
        pages: List[PDFPage] = []
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append({
                "page_num": str(i),
                "text": text.strip(),
                "char_count": str(len(text))
            })
        return pages

    def check_page_limit(self, max_pages: int = 20) -> None:
        page_count = len(self.content.get("text", []))
        if page_count > max_pages:
            raise ValueError(f"PDF has {page_count} pages, which exceeds the limit of {max_pages}.")

    def chunk_text(self, max_chars: int = 3000) -> List[str]:
        self._validate_text_content()
        chunks: List[str] = []
        for page in self.content["text"]:
            text = page["text"]
            page_num = page.get("page_num", "unknown")
            while len(text) > max_chars:
                chunks.append(f"[Page {page_num}] " + text[:max_chars])
                text = text[max_chars:]
            chunks.append(f"[Page {page_num}] " + text)
        return chunks

    def _validate_text_content(self) -> None:
        if "text" not in self.content or not isinstance(self.content["text"], list):
            raise ValueError("Missing or invalid 'text' field in PDF content.")
