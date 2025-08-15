# PDF Summary AI

## Objective
Design and implement a simple web application that allows users to upload big (up to 50MB, 100 pages) PDFs documents and receive AI-generated summaries using OpenAI's API.
## Core Features
- **PDF Upload**: Allow users to upload a PDF file.
- **PDF Parsing**: Make sure that PDFs with images and tables will be supported.
- **Summary Generation**: Use OpenAI's API to generate a summary of the uploaded PDF.
- **History Display**: Show the last 5 processed documents.

## How to run:

### Local:
1. Install dependencies
```
pip install -r requirements.yxy
```
2. Run app
```
streamlit run src/app.py
```
### Docker:

```
1. docker build -t pdf-summary-app .
2. docker run -p 8501:8501 pdf-summary-app

```

## 🧠 Tools

### 🔧 Stack
- **LangChain**: Chains for parsing, chunking, and summarizing
- **OpenAI**: GPT-4.1 for text, GPT-4o-mini for image captions

### 📄 Parsing, Chunking, Summarization
- `PyMuPDF4LLMLoader`: Page-wise loader with **table + image support**
- `LLMImageBlobParser`: GPT-powered **image recognition**
- `RecursiveCharacterTextSplitter`: Smart splits with overlap for better context