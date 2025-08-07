from langchain.output_parsers.retry import RetryWithErrorOutputParser
from langchain_core.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI 
from langchain_core.output_parsers import PydanticOutputParser 
from pydantic import BaseModel, Field 
from enum import Enum
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()

class EmailCategory(str, Enum): 
    PRIMARY = "Primary" 
    PROMOTIONAL = "Promotional" 
    ACTIONABLE = "Actionable" 

class ClassifiedEmail(BaseModel): 
    category: EmailCategory = Field(description="The final classification of the email.") 
    reasoning: str = Field(description="A brief explanation for the chosen category.") 

parser = PydanticOutputParser(pydantic_object=ClassifiedEmail)

format_instruction = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    """Analyze the email below and classify it. 
    {format_instructions} 
    Email Body: 
    {email_body}"""
]).partial(format_instructions=format_instruction)

retry_parser = RetryWithErrorOutputParser.from_llm(
    parser=parser, 
    llm=ChatOpenAI(model="gpt-4.1-nano",temperature=1.0)
)

model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)
chain = prompt | model | parser
retry_chain = prompt | model | retry_parser

try:
    # Format the prompt with your email content
    formatted_prompt = prompt.format(email_body="email_to_classify")

    # Run the LLM and get only the content (as a string)
    output = model.invoke(formatted_prompt).content
    print(output)
    # Parse the string output using retry parser
    result = retry_parser.parse_with_prompt(output, formatted_prompt)

    console.rule("[bold green]--- Parsed Output ---")
    print(f"Type: {type(result)}")
    console.print(Markdown(f"Category: {result.category.value}")) 
    console.print(Markdown(f"Reasoning: {result.reasoning}"))

except Exception as e:
    print(f"An Error Occurred: {e}")

