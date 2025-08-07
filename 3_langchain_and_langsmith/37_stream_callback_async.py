import asyncio 
from dotenv import load_dotenv 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.runnables import RunnableConfig 
from langchain_openai import ChatOpenAI 
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
load_dotenv() 

async def main():
    """ 
    Demonstrates programmatic access to a token stream using AsyncIteratorCallbackHandler. 
    """ 

    stream_handler = AsyncIteratorCallbackHandler()

    prompt = ChatPromptTemplate.from_template("Write a 3-line poem about {topic}.")

    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7, streaming=True)

    chain = prompt | model

    config: RunnableConfig = {
        "callbacks": [stream_handler]
    }

    print("--- Starting Streaming Chain ---")

    async def invoke_chain():
        await chain.ainvoke({"topic": "the ocean"}, config=config)

    task = asyncio.create_task(invoke_chain())

    full_response = ""

    async for token in stream_handler.aiter():
        print(token, end="", flush=True)
        full_response += token

    await task

    print("\n--- Streaming Finished ---")
    print(f"Full Response: \n{full_response}")
    # print(f"Total Tokens: {stream_handler}")
if __name__ == "__main__":
    asyncio.run(main())