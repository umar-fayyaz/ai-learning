from pydantic import BaseModel, Field
from typing import Optional, List 
from rich.console import Console
from rich.markdown import Markdown
from enum import Enum
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

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

full_parser = PydanticOutputParser(pydantic_object=ProcessedEmail)

full_format_instructions = full_parser.get_format_instructions()
# console.print(Markdown(full_format_instructions))

full_prompt = ChatPromptTemplate.from_template(
    """You are a hyper-efficient and accurate email processing agent. 
        Analyze the provided email and extract the required information precisely according to 
        the following JSON schema. 
        Do not add any commentary or introductory text. Your output must be only the valid 
        JSON object. 
        JSON Schema: 
        {format_instructions} 
        Email to Analyze: --- 
        From: {sender} 
        Subject: {subject} 
        Body: 
        {body} --- 
        """ 
).partial(format_instructions=full_format_instructions)

model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)
full_email_processing_chain = full_prompt | model | full_parser

complex_email = {
    "sender": "alice@corporate.com", 
    "subject": "Urgent Action: Finalize Q2 'Project Dragon' Report", 
    "body": """Hi team, 
    This is a critical reminder that the final report for Project Dragon needs to be submitted to me by this Friday, June 20th, 2025. 
    The report should include a full summary of our findings and a list of key achievements. Bob, please ensure your data tables are included. 
    The client presentation is scheduled for next Monday. This report is essential for that meeting. 
    Thanks, 
    Alice 
    """ 
}

try:
    console.rule("[bold green]--- Full Email Processing Result (as JSON) ---")
    result = full_email_processing_chain.invoke(complex_email)
    print(result.model_dump_json(indent=2))
except Exception as e:
    print(f"Error during full email processing: {e}")