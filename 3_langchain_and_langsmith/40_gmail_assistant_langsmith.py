import asyncio 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough 
from dotenv import load_dotenv 
from rich.console import Console 
from rich.markdown import Markdown 

console = Console()
load_dotenv()

async def run_complex_chain():

    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.0)

    sentiment_prompt = ChatPromptTemplate.from_template( 
        "Analyze the sentiment of the following email. Respond with a single word: Positive, Negative, or Neutral.\n\nEmail: {email_text}" 
    ) 

    summary_prompt = ChatPromptTemplate.from_template( 
        "Summarize the following email in a single, concise sentence.\n\nEmail: {email_text}" 
    ) 

    sentiment_chain = summary_prompt | model | StrOutputParser()

    summary_chain = sentiment_prompt | model | StrOutputParser()

    main_chain = RunnableParallel( 
        sentiment=RunnablePassthrough.assign(email_text=lambda x: x["email_text"]) | sentiment_chain, 
        summary=RunnablePassthrough.assign(email_text=lambda x: x["email_text"]) | summary_chain 
    ) 

    email_content = "Hi team, I just wanted to say thank you for all the hard work on the recent launch. The results have been phenomenal and I'm so proud of what we've accomplished together. Let's keep up the great momentum!" 

    console.rule("[bold green]--- Invoking complex chain ---")

    response = await main_chain.ainvoke({"email_text": email_content})

    console.print(Markdown(f"Response: {response}"))


if __name__ == "__main__":
    asyncio.run(run_complex_chain())