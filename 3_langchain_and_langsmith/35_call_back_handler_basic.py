import asyncio
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.callbacks.stdout import StdOutCallbackHandler
from dotenv import load_dotenv
load_dotenv()

async def main():
    """ 
    Demonstrates the use of a built-in callback handler to observe chain execution. 
    """ 
    stdout_handler = StdOutCallbackHandler()

    prompt = ChatPromptTemplate.from_template(
        "Tell me a short, inspiring story about a {subject}."
    )

    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)

    chain = prompt | model

    print("--- Invoking chain with StdOutCallbackHandler ---") 

    config: RunnableConfig = {
        "callbacks": [stdout_handler]
    }

    response = await chain.ainvoke({"subject":"software developer"}, config=config)

    print("\n--- Chain Execution finished ---")

    print(f"Final Response Content: \n{response.content}")

if __name__ == "__main__":
    asyncio.run(main())