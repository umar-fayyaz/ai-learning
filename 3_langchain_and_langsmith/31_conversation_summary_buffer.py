from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

summary_buffer_memory = ConversationSummaryBufferMemory(
    llm=model, 
    max_token_limit=100,
    memory_key="history",
    return_messages=True
)

