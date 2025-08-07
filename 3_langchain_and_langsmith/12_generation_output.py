import os 
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
load_dotenv()
console = Console()

model = ChatOpenAI(model="gpt-4.1-nano")

try:
    result = model.generate(
        messages=[[ 
            SystemMessage(content="You are a tokens counter assistant from given text."), 
            HumanMessage(content="Sun shining in the sky.") 
        ]]
    )
    console.rule("[bold green]--- LLM Result ---")
    print(result)

    console.rule("[bold red]--- First Generation ---")

    first_generation = result.generations[0][0] 
    print(first_generation)

    console.rule("[bold blue]--- Generation's Message ---") 
    ai_message = first_generation.message 
    print(ai_message) 
    print("Content:", ai_message.content) 
    
    console.rule("[bold yellow]\n--- Generation Info ---") 
    print(first_generation.generation_info) 

    console.rule("[bold brown]\n--- Aggregated Token Usage ---") 
    print(result.llm_output['token_usage']) 

except Exception as e:
    print(f"Error during sync invocation (ensure API key is set): {e}")