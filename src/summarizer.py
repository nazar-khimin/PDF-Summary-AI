from langchain.chains.summarize import load_summarize_chain

from openai_clients import get_gpt_4_1


def summarize_pdf(docs):
    if not docs:
        return "No documents to summarize."

    chain = load_summarize_chain(
        llm= get_gpt_4_1(),
        chain_type="map_reduce"
    )
    return chain.invoke({"input_documents": docs})["output_text"]