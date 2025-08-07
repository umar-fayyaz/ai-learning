from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.console import Console
from rich.markdown import Markdown
# import asyncio


from dotenv import load_dotenv
load_dotenv()
console = Console()

chat_model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

string_parser = StrOutputParser()

prompt_template = ChatPromptTemplate.from_template("Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner.")

explanation_chain = (
    RunnablePassthrough() 
    | prompt_template 
    | chat_model 
    | string_parser
)

console.rule("\n[bold blue]--- Schema Inspection ---")

print("Prompt Template Input Schema:", prompt_template.input_schema.model_json_schema()) 

# # Expected output: {'title': 'PromptInput', 'type': 'object', 'properties': {'user_topic': {'title': 'User Topic', 'type': 'string'}}} (or similar) 

# print("\n\n\n\nPrompt Template Output Schema:", prompt_template.output_schema.model_json_schema()) 

# print("\n\n\n\nChat Model Input Schema:", chat_model.input_schema.model_json_schema()) # Will be BasePromptValue or str/list of messages

# print("\n\n\n\nChat Model Output Schema:", chat_model.output_schema.model_json_schema()) # Will be AIMessage 

# print("\n\n\n\nString Parser Input Schema:", string_parser.input_schema.model_json_schema()) # Will be AIMessage, SystemMessage, etc. 

# print("\n\n\n\nString Parser Output Schema:", string_parser.output_schema.model_json_schema()) # Will be str 

# print("\n\n\n\nExplanation Chain Input Schema:", explanation_chain.input_schema.model_json_schema()) 

# print("\n\n\n\nExplanation Chain Output Schema:", explanation_chain.output_schema.model_json_schema()) 

