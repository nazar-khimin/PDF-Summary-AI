from typing import Iterator

from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from openai_clients import get_gpt_4_mini_llm
from tiktoken import get_encoding


def summarize_pdf(documents: list[Document]):
    if not documents:
        raise ValueError("No documents provided for summarization.")

    initial_prompt = PromptTemplate(
        input_variables=["text"],
        template="Write a summary of this text:\n{text}"
    )

    refine_prompt = PromptTemplate(
        input_variables=["existing_summary", "text"],
        template=(
            "Here is an existing summary: {existing_summary}\n"
            "Here is some more text: {text}\n"
            "Refine the existing summary with this new information."
        )
    )

    chain = load_summarize_chain(
        llm=get_gpt_4_mini_llm(),
        chain_type="refine",
        question_prompt = initial_prompt,
        refine_prompt = refine_prompt,
        verbose=True
    )
    return chain.invoke({"input_documents": documents})["output_text"]


def get_token_count(doc: Document) -> int:
    encoding = get_encoding("cl100k_base")
    return len(encoding.encode(doc.page_content))
