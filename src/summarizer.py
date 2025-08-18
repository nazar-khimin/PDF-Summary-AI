from typing import Iterator, List

from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from openai_clients import get_gpt_4_mini_llm
from tiktoken import get_encoding


def summarize_pdf(documents: Iterator[Document]):
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
        initial_response_name="existing_summary",
        verbose=True
    )
    document_list = list(documents)
    print_token_usage(document_list)
    return chain.invoke({"input_documents": document_list})["output_text"]

def get_token_count(doc: Document) -> int:
    encoding = get_encoding("cl100k_base")
    return len(encoding.encode(doc.page_content))

def print_token_usage(documents: List[Document]) -> None:
    total_tokens = sum(get_token_count(doc) for doc in documents)
    print(f"🔢 Total tokens: {total_tokens}")

    print("📄 Token count per page:")
    for i, doc in enumerate(documents):
        token_count = get_token_count(doc)
        print(f"• Page {i + 1}: {token_count} tokens")