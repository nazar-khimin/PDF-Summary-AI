import io
import streamlit as st
from dotenv import load_dotenv
from streamlit_pdf_viewer import pdf_viewer
from pdf_loader import load_pdf
from summarizer import summarize_pdf

load_dotenv()
st.set_page_config(page_title="📄 PDF Summarizer", layout="centered")
st.title("📄 PDF Summarizer")

# ─────────────────────────────────────────────────────────────
# Session‐state initialization
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
if "last_uploaded_name" not in st.session_state:
    st.session_state.last_uploaded_name = None

# ─────────────────────────────────────────────────────────────
# File uploader
uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_pdf and uploaded_pdf.name != st.session_state.last_uploaded_name:
    st.session_state.last_uploaded_name = uploaded_pdf.name
    st.session_state.selected_index = None

# ─────────────────────────────────────────────────────────────
# Summarize on button click
if uploaded_pdf and st.button("Summarize"):
    with st.spinner(f"Summarizing {uploaded_pdf.name}…"):
        try:
            pdf_bytes: io.BytesIO = io.BytesIO(uploaded_pdf.read())
            document_list = load_pdf(pdf_bytes)
            summary = summarize_pdf(document_list)
            st.session_state.history.insert(0, {
                "name": uploaded_pdf.name,
                "summary": summary,
                "pdf_bytes": pdf_bytes
            })
            if len(st.session_state.history) > 5:
                st.session_state.history.pop()
            st.session_state.selected_index = 0
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ─────────────────────────────────────────────────────────────
# Sidebar navigator
st.sidebar.header("🕘 Recent Summaries")
if st.session_state.history:
    placeholder = "— Select a document —"
    opts = [placeholder] + [r["name"] for r in st.session_state.history]
    idx = st.session_state.selected_index
    default = idx + 1 if idx is not None else 0
    choice = st.sidebar.selectbox("Choose a document", opts, index=default)
    st.session_state.selected_index = opts.index(choice) - 1 if choice != placeholder else None
else:
    st.sidebar.info("No summaries yet")

# ─────────────────────────────────────────────────────────────
# Display summary & PDF
if st.session_state.selected_index is not None:
    record = st.session_state.history[st.session_state.selected_index]
    st.subheader(f"Summary:")
    st.markdown(record["summary"])
    with st.expander("📄 View PDF"):
        pdf_viewer(input=record["pdf_bytes"], width="100%", height=600)
