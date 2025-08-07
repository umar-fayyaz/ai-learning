import asyncio 
from langsmith import traceable 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 

load_dotenv()

@traceable(run_type="tool", name="Clean Email Text V2") 
def clean_email_text(raw_text: str) -> str: 
    """Removes boilerplate signatures and legal disclaimers.""" 
    # In a real scenario, this could use regex or other logic 
    cleaned_text = raw_text.split("---")[0].strip() 
    return cleaned_text 

async def run_traceable_chain(): 
    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.0) 
    prompt = ChatPromptTemplate.from_template("Summarize this: {cleaned_text}") 
     
    # We can compose our custom function directly into the chain! 
    chain = { 
        "cleaned_text": lambda x: clean_email_text(x["raw_email"]) 
    } | prompt | model | StrOutputParser() 
 
    email_with_signature = "This is the core message.\n---\nRegards, Bob\nLegal Disclaimer: ... " 
     
    print("Invoking chain with traceable function...") 
    response = await chain.ainvoke({"raw_email": email_with_signature}) 
    print("Response:", response) 

if __name__ == "__main__":
    asyncio.run(run_traceable_chain())