from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.console import Console
from rich.markdown import Markdown
import asyncio


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

console.rule("\n[bold blue]--- Synchronous Streaming ---")

try:

    for chunk in explanation_chain.stream({"user_topic": "artificial intelligence"}):
        console.print(chunk,end="")
except Exception as e:
    print(f"Error during sync invocation: {e}")

async def main_async_stream():
    console.rule("\n[bold blue]--- Asynchronous Streaming ---")
    try:

        async for chunk in explanation_chain.astream({"user_topic": "machine learning"}):
            console.print(chunk,end="")
    except Exception as e:
        print(f"Error during async invocation: {e}")

if __name__ == "__main__":
    asyncio.run(main_async_stream())