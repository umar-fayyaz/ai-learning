from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from rich.console import Console
from dotenv import load_dotenv
import asyncio
load_dotenv()

console = Console()

chat_model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.1)

async def call_model_directly():

    messages = [
        SystemMessage(content="You are a terse and witty tech commentator."),
        HumanMessage(content="What is your opinion on the future of AI?")
    ]

    console.rule("[bold yellow]--- Synchronous Call ---")
    sync_response = chat_model.invoke(messages)
    console.print(sync_response.content)

    console.rule("[bold green]--- Asynchronous Call ---")
    async_response = await chat_model.ainvoke(messages)
    console.print(async_response.content)

    console.rule("[bold blue]--- Asynchronous Streaming ---")
    async for chunk in chat_model.astream(messages):
        console.print(chunk.content, end="")

if __name__ == "__main__":
    asyncio.run(call_model_directly())