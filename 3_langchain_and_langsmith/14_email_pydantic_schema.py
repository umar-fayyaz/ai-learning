from pydantic import BaseModel, Field
from typing import Optional, List 
from rich.console import Console
from rich.markdown import Markdown
from enum import Enum

console = Console()

class EmailCategory(str, Enum):
    """Enum for possible email categories.""" 

    PRIMARY="Primary"
    SPAM="Spam"
    ACTIONABLE="Actionable"
    PROMOTIONAL="Promotional"

class ExtractedEntity(BaseModel):
    """Represents a single named entity extracted from the email.""" 

    text:str = Field(description="The actual text of the extracted entity (e.g., 'Project Phoenix', 'next Tuesday').")
    type:str = Field(description="The type of the entity (e.g., 'Project Name', 'Data', 'Person').")

class ActionItem(BaseModel):
    """Represents a single action item or task identified in the email.""" 
    description:str = Field(description="A clear and concise description of the task.")
    due_date: Optional[str] = Field(None, description="The suggested due date for the action, if any, in YYYY-MM-DD format.")
    assignee:Optional[str] = Field(None, description="The person or team assigned to the task, if mentioned.")

class ProcessedEmail(BaseModel):
    """The final, structured output after analyzing an email.""" 
    category: EmailCategory = Field(description="The main classification of the email.") 
    subject: str = Field(description="The subject line of the email.") 
    summary: str = Field(description="A one-sentence summary of the email's content.") 
    entities: List[ExtractedEntity] = Field(description="A list of key named entities found in the email.") 
    action_items: List[ActionItem] = Field(description="A list of specific action items or tasks requested in the email.") 
    sentiment: str = Field(description="The overall sentiment of the email (e.g., 'Positive', 'Neutral', 'Negative').")

example_processed_email = ProcessedEmail( 
category=EmailCategory.ACTIONABLE, 
    subject="Project Phoenix - Next Steps", 
    summary="Alice requires the final report by next Tuesday to prepare for the client meeting.", 
    entities=[ 
        ExtractedEntity(text="Alice", type="Person"),
        ExtractedEntity(text="Project Phoenix", type="Project Name"), 
        ExtractedEntity(text="next Tuesday", type="Date") 
    ], 
    action_items=[ 
        ActionItem( 
            description="Prepare the final report for Project Phoenix.", 
            due_date="2025-06-17", # Assuming today is around June 10, 2025 
            assignee="Me" 
        ),
        ActionItem( 
            description="Send the report to Alice.", 
            due_date="2025-06-17", 
            # assignee="Me" 
        ) 
    ], 
    sentiment="Neutral" 
)

print(example_processed_email.model_dump_json(indent=2))