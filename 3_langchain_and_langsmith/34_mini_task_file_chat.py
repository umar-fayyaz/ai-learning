from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import json
from pathlib import Path
from typing import List, Sequence
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict, messages_to_dict
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

class FileChatMessageHistory(BaseChatMessageHistory):
    """Custom chat history stored in a JSON file.""" 

    def __init__(self, session_id:str, file_path: str="3_langchain_and_langsmith/32_chat_sessions"):
        self.session_id = session_id
        self.file_path = Path(file_path)/f"{session_id}.json"
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def messages(self)-> List[BaseMessage]:
        """Retrieve messages from the file.""" 
        if not self.file_path.exists():
            return []
        with self.file_path.open("r") as f:
            return messages_from_dict(json.load(f))
        
    def add_message(self, message:Sequence[BaseMessage])->None:
        """Append messages to the file.""" 
        stored_messages = self.messages
        if isinstance(message, BaseMessage):
            message = [message]
        all_messages = messages_to_dict(stored_messages + list(message))
        with self.file_path.open("w") as f:
            json.dump(all_messages, f, indent=2)

    def clear(self)->None:
        """Clear the file.""" 
        if self.file_path.exists():
            self.file_path.unlink()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return FileChatMessageHistory(session_id=session_id)

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

    config_user_2 = {"configurable": {"session_id": "user_2"}} 
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

    history_1 = FileChatMessageHistory("user_1")
    print("\nUser 1 History:")
    
    for msg in history_1.messages:
        print(f"{msg.type}: {msg.content}")

    history_2 = FileChatMessageHistory("user_2")
    print("\nUser 2 History:")
    for msg in history_2.messages:
        print(f"{msg.type}: {msg.content}")
 

if __name__ == "__main__":
    asyncio.run(run_conversation())