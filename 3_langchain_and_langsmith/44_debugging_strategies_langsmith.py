import asyncio 
from typing import List, Optional 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate 
from pydantic import BaseModel, Field 
from langchain_core.output_parsers import PydanticOutputParser 
from dotenv import load_dotenv 

load_dotenv()

class ActionItem(BaseModel): 
    task: str = Field(description="The specific action item to be completed.") 
    assignee: Optional[str] = Field(description="The person or team assigned to the task.") 
    deadline: Optional[str] = Field(description="The deadline for the action item.") 
    # user_name: str = Field(description="The priority of the action item.") 
    # user_created: int = Field(description="The person or team assigned to the task. The deadline for the action item. The specific action item to be completed.")


class ActionItems(BaseModel): 
    items: List[ActionItem]

async def run_failing_chain():
    parser = PydanticOutputParser(pydantic_object=ActionItems) 
    prompt = ChatPromptTemplate.from_messages([ 
        ("system", "You are an expert at extracting action items from text. Please respond with a JSON object containing the action items, formatted according to the provided schema."), 
        ("human", "From this email, please extract all action items.\n\nEmail: {email_text}\n\n{format_instructions}") 
    ]).partial(format_instructions=parser.get_format_instructions()) 

    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0) 

    chain = prompt | model | parser 

    ambiguous_email = "Hey team, just thinking about the project. We should probably consider the new marketing angles soon. Also, someone should look into the Q3 budget. Thanks." 

    print("Invoking chain that might fail...") 

    try:

        response = await chain.with_config({"tags": ["debugging-test"]}).ainvoke({"email_text": ambiguous_email}) 

        print("Success!", response) 

    except Exception as e:
        print("Chain failed with error:", e)

if __name__ == "__main__":
    asyncio.run(run_failing_chain())