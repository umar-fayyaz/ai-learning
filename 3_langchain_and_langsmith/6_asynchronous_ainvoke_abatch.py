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

prompt_template = ChatPromptTemplate.from_template("Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner.")

string_parser = StrOutputParser()

explanation_chain = (
    RunnablePassthrough() 
    | prompt_template 
    | chat_model 
    | string_parser
)

async def main_async_invoke():
    console.rule("\n[bold blue]--- Asynchronous Single Invocation ---")

    try:
        result_async_single = await explanation_chain.ainvoke({"user_topic": "artificial intelligence"})
        console.print(Markdown(f"Async Single Invocation Result:\n{result_async_single}"))
    except Exception as e:
        print(f"Error during async single invocation (ensure API key is set): {e}")


async def main_async_batch():
    console.rule("\n[bold blue]--- Asynchronous Batch Invocation ---")
    inputs_async_batch = [ 
        {"user_topic": "string theory"}, 
        {"user_topic": "loop quantum gravity"} 
        ]
    try:
        results_async_batch = await explanation_chain.abatch(inputs_async_batch)
        console.print(Markdown(f"Async Batch Invocation Results:\n"))
        for i,res in enumerate(results_async_batch):
            console.print(Markdown(f"{inputs_async_batch[i]['user_topic']}: \n{res}\n"))
    except Exception as e:
        print(f"Error during async batch invocation: {e}")

if __name__ == "__main__":
    asyncio.run(main_async_invoke())
    asyncio.run(main_async_batch())