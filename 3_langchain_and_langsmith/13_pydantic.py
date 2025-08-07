from pydantic import BaseModel, Field
from typing import Optional, List 
from rich.console import Console
from rich.markdown import Markdown

console = Console()

class UserProfile(BaseModel):
    """A Pydantic model to represent a user's profile.""" 

    username:str = Field(description="The user's unique username.") 
    user_id:int = Field(description="The user's integer ID.")
    email: Optional[str] = Field(None, description="The user's optional email address.")
    interests: List[str] = Field(description="A list of the user's interests.")

try:
    # user = UserProfile(
    #     username="umar_fayyaz",
    #     user_id=123,
    #     interests=["AI","Python", "hiking"]
    # )
    # console.rule("[bold yellow]Successfully created UserProfile instance:")
    # print(user.model_dump_json(indent=2))
    # print(user)

    # This would raise a validation error because user_id is not an integer 
    invalid_user = UserProfile( 
        username="jane_doe", 
        user_id="not_an_int", # <-- Error here 
        interests=["art", "history"] 
    )

except Exception as e:
    console.rule("[bold red]Error creating UserProfile instance:")
    print(e)

