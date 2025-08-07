from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
load_dotenv()
console = Console()

chat_model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

slogan_template = ChatPromptTemplate.from_template("Create a short, catchy marketing slogan for the product: '{product_name}'.")

# slogan_template = ChatPromptTemplate.from_template("Find and write the original slogan or tagline of given product: '{product_name}'.")

string_parser = StrOutputParser()

# Method 2: Using RUnnable Passthrough
slogan_chain = (
    RunnablePassthrough() 
    | slogan_template 
    | chat_model 
    | string_parser
)

# --- Asynchronous Invocation

async def get_slogan(product_dict):
    return await slogan_chain.ainvoke(product_dict)

async def main_async():
    console.rule("\n[bold blue]--- Asynchronous Invocation ---")
    
    product_input_async = {"product_name": "Iphone 17 Pro Max"} 

    try:
        async_slogan = await get_slogan(product_input_async)
        console.print(Markdown(f"Slogan for '{product_input_async['product_name']}':\n{async_slogan}"))
    except Exception as e:
        print(f"Error during async invocation (ensure API key is set): {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())




