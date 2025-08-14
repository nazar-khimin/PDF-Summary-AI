import streamlit as st
from io import BytesIO
from logic_facade import load_pdf, generate_summary

MAX_PAGES = 100
CHUNK_SIZE = 3000
SESSION_KEY = "pdf_data"

# Session Management
def save_pdf_to_session(name: str, file: BytesIO) -> None:
    st.session_state[SESSION_KEY] = {
        "name": name,
        "data": file.getvalue()
    }

def get_pdf_from_session() -> tuple[str, BytesIO] | None:
    pdf_info = st.session_state.get(SESSION_KEY)
    if not pdf_info:
        return None
    return pdf_info["name"], BytesIO(pdf_info["data"])

# UI Components
def upload_pdf_ui() -> None:
    uploaded_file = st.file_uploader("Upload a PDF (max 100 pages)", type=["pdf"])
    if uploaded_file:
        save_pdf_to_session(uploaded_file.name, uploaded_file)

def summary_ui(name: str, chunks: list[str]) -> None:
    if st.button("📝 Generate Summary"):
        with st.spinner("Summarizing..."):
            summary = generate_summary(chunks)
        st.success("✅ Summary generated!")
        st.text_area("Summary", summary, height=400)

def main() -> None:
    st.set_page_config(page_title="PDF Summary AI", page_icon="📄")
    st.title("📄 PDF Summarizer & Chat")

    upload_pdf_ui()

    pdf_info = get_pdf_from_session()
    if not pdf_info:
        return

    name, file = pdf_info

    try:
        with st.spinner(f"Loading '{name}'..."):
            processor = load_pdf(file, max_pages=MAX_PAGES)
            page_count = processor.get_page_count()
            chunks = processor.chunk_text(max_chars=CHUNK_SIZE)

        st.success(f"✅ Loaded '{name}' ({page_count} pages, {len(chunks)} chunks).")
        summary_ui(name, chunks)

        st.subheader("💬 Chat with your PDF (coming soon...)")

    except ValueError as ve:
        st.error(str(ve))
    except Exception as e:
        st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
