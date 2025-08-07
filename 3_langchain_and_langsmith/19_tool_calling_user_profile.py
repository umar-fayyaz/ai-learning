from pydantic import BaseModel, Field
from typing import Optional, List 
from rich.console import Console
from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv()

console = Console()

chat_model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

class UserProfile(BaseModel):
    """A Pydantic model to represent a user's profile."""
    username:str = Field(description="The user's unique username.")
    user_id:int = Field(description="The user's integer ID.")
    email: Optional[str] = Field(None, description="The user's optional email address.")
    interests: List[str] = Field(description="A list of the user's interests.")

structured_llm = chat_model.with_structured_output(UserProfile)

try:
    console.rule("[bold yellow]\n--- Structured Output Example ---]")
    user_description = "The user is jsmith, their ID is 9988. They love rock climbing, sci-fi novels, and their email is jsmith@example.com."

    structured_response = structured_llm.invoke(user_description)
    print("Type of response: ", type(structured_response))
    print("\nStrcutured Response (as Pydantic Object)")
    print(structured_response)

    console.rule("[bold green]\nAccessing Data: ")
    print(f"Username: {structured_response.username}")
    print(f"User ID: {structured_response.interests}")

    console.rule("[bold red]\nJSON representation: ")
    print(structured_response.model_dump_json(indent=2))

except Exception as e:
    print(f"Error during structured output: {e}")