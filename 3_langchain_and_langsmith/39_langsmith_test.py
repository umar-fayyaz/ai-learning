import asyncio 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from dotenv import load_dotenv 
from rich.console import Console 
from rich.markdown import Markdown 

load_dotenv()

console = Console()

async def run_simple_chain():

    prompt = ChatPromptTemplate.from_template("Tell me a one-sentence joke about {topic}.")

    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.0)

    parser = StrOutputParser()

    chain = prompt | model | parser

    console.rule("[bold green]--- Running Simple Chain ---")

    response = await chain.ainvoke({"topic": "Data Science"})

    console.print(Markdown(f"Response: {response}"))

if __name__ == "__main__":
    asyncio.run(run_simple_chain())