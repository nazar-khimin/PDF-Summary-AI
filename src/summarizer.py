from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from openai_clients import get_gpt_4o_mini_llm, get_gpt_5

def summarize_pdf(docs):
    if not docs:
        return "No documents to summarize."

    def summarize_chunk(doc):
        chain = load_summarize_chain(
            llm=get_gpt_4o_mini_llm(),
            chain_type="stuff"
        )
        result = chain.invoke({"input_documents": [doc]})
        return result["output_text"]

    with ThreadPoolExecutor(max_workers=2) as executor:
        chunk_summaries = list(
            tqdm(
                executor.map(summarize_chunk, docs),
                total=len(docs),
                desc="Summarizing chunks",
                dynamic_ncols=True
            )
        )

    combined_doc = Document(page_content="\n\n".join(chunk_summaries))
    chain = load_summarize_chain(
        llm=get_gpt_5(),
        chain_type="stuff"
    )
    final_result = chain.invoke({"input_documents": [combined_doc]})
    return final_result["output_text"]
