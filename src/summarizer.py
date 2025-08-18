from typing import Iterator, List

from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from openai_clients import get_gpt_4_mini_llm
from tiktoken import get_encoding


def summarize_pdf(documents: Iterator[Document]):
    if not documents:
        raise ValueError("No documents provided for summarization.")

    document_list = list(documents)
    print_token_usage(document_list)

    initial_prompt = ChatPromptTemplate.from_messages([
        ("system", """Your name is PDF Summarizer. You are a professional summarizer who works with PDFs containing text, tables, and images. Your task is to create a concise and comprehensive summary of the provided content,
     whether it's an article, finance analytics or conversation.
     
     Guidelines:
     - Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.
     - Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
     - When the input includes tabular data, analyze and interpret key trends or comparisons.
     - When the input includes image descriptions or OCR, describe the visual content in context.
     - Rely strictly on the provided content, without including external information.
     - Format the summary in paragraph form for easy understanding.
    """),
        ("human", "{task_instruction}:\n\n{text}")
    ])

    refine_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are refining an existing summary based on new content from a PDF.  Update the summary to include any new insights, trends, or important details. 
        Maintain clarity, conciseness, and structure. Do not repeat information.

        Existing Summary:
        {existing_summary}
    
        New Content:
        {content}"""),
            ("human", "{task_instruction}")
        ])

    chain = load_summarize_chain(
        llm=get_gpt_4_mini_llm(),
        chain_type="refine",
        question_prompt=initial_prompt,
        refine_prompt=refine_prompt,
        document_variable_name = "text"
    )

    summary = chain.invoke({
        "task_instruction" : "Summarize the following contents:",
        "input_documents": document_list
    })

    return summary["output_text"]

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