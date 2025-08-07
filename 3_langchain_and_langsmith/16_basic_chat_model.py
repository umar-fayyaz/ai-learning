from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown
# from typing import List,Optional

import asyncio


from dotenv import load_dotenv
load_dotenv()
console = Console()

async def set_model(temperature:float):
    try:
        chat_model = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=temperature,
        max_tokens=1000,
        # streaming=True
    )
        return chat_model
    except Exception as e:
        print(f"Error: {e}")
        return None

async def llm_invoke(message, chat_model):
    if chat_model:
        try:
            result = await chat_model.ainvoke(message)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        print("Chat model is not set.")
        return None

async def display_reult(temperature):
    message = [HumanMessage(content="Write a 100 words describing a cat.")]
    set_model_result = await set_model(temperature)
    if set_model:
        result = await llm_invoke(message, set_model_result)
        if result:
            console.rule(f"\n\nOutput of Temperature: {temperature}\n")
            print(result.content)
        else:
            print("Result is None.")

async def main():
    await display_reult(0.1)
    await display_reult(1.2)

if __name__ == "__main__":
    asyncio.run(main())