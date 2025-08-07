from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from dotenv import load_dotenv
load_dotenv()
import asyncio

prompt = ChatPromptTemplate.from_messages([ 
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability."), 
    MessagesPlaceholder(variable_name="history"), 
    ("human", "{input}"), 
])

model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)

chain = prompt | model

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(
    chain, 
    get_session_history,
    input_messages_key="input", 
    history_messages_key="history"
)

config_user_1 = {"configurable": {"session_id": "user_1"}} 

async def run_conversation():
    response1 = await with_message_history.ainvoke(
        {"input": "Hi! I'm John from Lahore."},
        config=config_user_1
    )
    print(f"AI: {response1.content}")

    response2 = await with_message_history.ainvoke(
        {"input": "What's my name and where am I from?"}, 
        config=config_user_1 
    ) 
    print(f"AI: {response2.content}") 

    config_user_2 = {"configurable": {"session_id": "user_1"}} 
    response = await with_message_history.ainvoke( 
        {"input": "Hi! I'm Sarah."}, 
        config=config_user_2 
    ) 
    print(f"AI: {response.content}") 

    response = await with_message_history.ainvoke(
        {"input": "What is my name?"},
        config=config_user_2 
    ) 
    print(f"AI: {response.content}")
    # print(store)
    print("\nUser 1 History:") 
    print(store["user_1"].messages) 
    print("\nUser 2 History:") 
    print(store["user_2"].messages) 

if __name__ == "__main__":
    asyncio.run(run_conversation())

