from typing import Iterator, List

from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from tiktoken import get_encoding

from openai_clients import get_gpt_4_mini_llm


def summarize_pdf(documents: Iterator[Document]):
    if not documents:
        raise ValueError("No documents provided for summarization.")

    document_list = list(documents)
    print_token_usage(document_list)

    # Processes each document chunk
    map_prompt = ChatPromptTemplate.from_messages([
        ("system", """Your name is PDF Summarizer. 
    You are a professional summarizer who works with PDFs containing text, tables, and images.

    Guidelines:
    - {length_instruction}
    - Maintain clarity, accuracy, and focus.
    - Incorporate main ideas and essential information.
    - When the input includes tabular data, interpret key trends or comparisons.
    - When the input includes image descriptions or OCR, describe the visual content in context.
    - Rely strictly on the provided content, with no external additions.
    - Format according to the requested length style.
    """),
        ("human", "{task_instruction}:\n\n{text}")
    ])

    # Merges the chunk summaries
    combine_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a summarization expert tasked with synthesizing multiple summaries into one cohesive, comprehensive summary.

    Guidelines:
    - {length_instruction}
    - Integrate key insights from all summaries.
    - Remove redundancy, ensure logical flow.
    - Preserve clarity and match the requested length style.
    """),
        ("human", "{task_instruction}:\n\n{text}")
    ])

    chain = load_summarize_chain(
        llm=get_gpt_4_mini_llm(),
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
    )

    summary = chain.invoke({
        "task_instruction": "Summarize the following contents:",
        "length_instruction": get_style_by_length(len(document_list)),
        "input_documents": document_list
    })

    return summary["output_text"]


def get_style_by_length(page_count: int) -> str:
    """
    Decide summary guideline based on page count and return the instruction text.
    """
    length_guidelines = {
        "short": (
            "Limit output to a single sentence (max 280 characters)."
            "Where helpful, add a short bullet list highlighting the most important points."
        ),
        "medium": (
            "Limit output to one concise paragraph (3–5 sentences)."
            "Where helpful, add a short bullet list highlighting the most important points."
        ),
        "long": (
            "Provide a detailed summary in **no more than 2 paragraphs**. "
            "Include key trends, context, and nuances. "
            "Where helpful, add a short bullet list highlighting the most important points."
        )
    }

    if page_count <= 2:
        mode = "short"
    elif page_count <= 10:
        mode = "medium"
    else:
        mode = "long"

    return length_guidelines[mode]


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