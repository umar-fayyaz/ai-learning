import asyncio 
from dotenv import load_dotenv 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI 
# from langchain.callbacks import OpenAICallbackHandler
from langchain_community.callbacks.openai_info import OpenAICallbackHandler

load_dotenv() 

async def track_cost():

    prompt = ChatPromptTemplate.from_template("Explain the concept of {topic} in one paragraph")

    model = ChatOpenAI(model="gpt-4.1-nano")

    chain = prompt | model

    cost_handler = OpenAICallbackHandler()
    chain = chain.with_config({"callbacks": [cost_handler]})

    await chain.ainvoke({"topic": "quantum computing"})

    await chain.ainvoke({"topic": "machine learning"})

    print("\n--- Cost and Token Information ---") 
    print(f"Total Tokens: {cost_handler.total_tokens}") 
    print(f"Prompt Tokens: {cost_handler.prompt_tokens}") 
    print(f"Completion Tokens: {cost_handler.completion_tokens}") 
    print(f"Total Cost (USD): ${cost_handler.total_cost:.10f}") 

if __name__ == "__main__":
    asyncio.run(track_cost())