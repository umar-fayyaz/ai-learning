import json
from pathlib import Path
from typing import List, Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict, messages_to_dict


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

# try:
custom_history = FileChatMessageHistory(session_id="custom_session_1")
custom_history.add_user_message("This is a 2nd test custom file history")
custom_history.add_ai_message("I see your 2nd test, and it is stored.")
print(custom_history.messages)

# except Exception as e:
#     print(f"Error: {e}")