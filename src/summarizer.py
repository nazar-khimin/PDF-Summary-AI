from typing import Iterator

from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from openai_clients import get_gpt_4_mini_llm


def summarize_pdf(documents: Iterator[Document]):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "]
    )

    splitter.split_documents(documents)

    if not documents:
        return "No documents to summarize."

    chain = load_summarize_chain(
        llm=get_gpt_4_mini_llm(),
        chain_type="map_reduce"
    )
    return chain.invoke({"input_documents": documents})["output_text"]
