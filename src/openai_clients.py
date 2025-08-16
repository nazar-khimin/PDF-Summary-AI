from langchain_openai import ChatOpenAI


# mode for chunk and final summarization
def get_gpt_4_mini_llm():
    return ChatOpenAI(model="gpt-4.1-mini", temperature=0.1, max_tokens=2000)

# model for image recognition
def get_gpt_4_nano_llm():
    return ChatOpenAI(model="gpt-4.1-nano", temperature=0.1, max_tokens=2000)