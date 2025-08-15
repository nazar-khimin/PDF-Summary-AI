from langchain_openai import ChatOpenAI


def get_gpt_4o_mini_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=128)

def get_gpt_4_1():
    return ChatOpenAI(model="gpt-4.1", temperature=0, max_tokens=128)


def get_gpt5_mini_llm():
    return ChatOpenAI(model="gpt-5-mini", temperature=0, max_tokens=512)