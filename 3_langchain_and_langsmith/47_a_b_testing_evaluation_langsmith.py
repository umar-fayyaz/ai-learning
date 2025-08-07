import asyncio 
from typing import Dict 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langsmith import Client 
from i46_custom_evaluation_langsmith import check_category_match 
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv 
from rich.console import Console 
from rich.markdown import Markdown 
console = Console()

load_dotenv()

def create_classification_chain(prompt_template:str, model: ChatOpenAI) -> Dict:

    prompt = ChatPromptTemplate.from_template(prompt_template)

    chain = prompt | model | StrOutputParser()

    return RunnablePassthrough.assign(category=chain)

async def main():
    client = Client()

    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

    # prompt version 1 
    prompt_v1 = "Classify the following email into one of three categories: Primary, Spam, or Actionable.\n\nEmail: {email_text}\n\nCategory:"

    chain_v1 = create_classification_chain(prompt_v1, model)

    # prompt version 2
    prompt_v2 =  """ 
    You are an email classification expert. Your task is to classify an email into exactly one of the following three categories: 
    - Primary: A standard, non-urgent personal or professional message. 
    - Spam: An unsolicited marketing or malicious email. 
    - Actionable: An email that explicitly requires the recipient to perform a task. 
     
    Respond with a single word only. 
    Email: {email_text} 
    Category: 
    """

    chain_v2 = create_classification_chain(prompt_v2, model)

    # run test for prompt v1
    console.rule("[bold yellow]Running A/B Test for Prompt Version 1")

    client.run_on_dataset(
        dataset_name="Gmail Classification (Eval V1)",
        llm_or_chain_factory=lambda: chain_v1,
        custom_evaluators=[check_category_match],  # ✅ fixed here
        project_name="gmail-assistant-eval-v1",  # Send runs to a new project for comparison
        concurrency_level=5,
    )

    console.print(Markdown("### A/B Test for Prompt Version 1 completed."))

    # run test for prompt v2
    console.rule("[bold yellow]Running A/B Test for Prompt Version 2")

    client.run_on_dataset(
        dataset_name="Gmail Classification (Eval V1)",
        llm_or_chain_factory=lambda: chain_v2, 
        custom_evaluators=[check_category_match],
        project_name="gmail-assistant-eval-v2", # Send runs to a new project for comparison
        concurrency_level=5,
    )

    console.print(Markdown("### A/B Test for Prompt Version 2 completed."))

if __name__ == "__main__":
    asyncio.run(main())