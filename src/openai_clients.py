from langchain_openai import ChatOpenAI


def get_gpt_4o_mini_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=2000)

def get_gpt_4_1():
    return ChatOpenAI(model="gpt-4.1", temperature=0, max_tokens=2000)

def get_gpt_5():
    return ChatOpenAI(model="gpt-5", temperature=0, max_tokens=2000)