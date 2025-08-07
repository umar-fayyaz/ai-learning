from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.console import Console
from rich.markdown import Markdown
import os

from dotenv import load_dotenv
load_dotenv()
console = Console()

chat_model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

prompt_template = ChatPromptTemplate.from_template("Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner.")

string_parser = StrOutputParser()

# Method 1 Simple direct chain
# explanation_chain = prompt_template | chat_model | string_parser

# Method 2: Using RUnnable Passthrough
explanation_chain = (
    RunnablePassthrough() 
    | prompt_template 
    | chat_model 
    | string_parser
)

#  --- Try it out (Synchronous Invocation) --- 
# console.rule("\n[bold blue]--- Synchronous Invocation ---") 
# topic_input = {"user_topic": "quantum entanglement"} 

# try: 
#     sync_explanation = explanation_chain.invoke(topic_input) 
#     console.print(Markdown (f"Explanation for '{topic_input['user_topic']}':\n{sync_explanation}"))
# except Exception as e: 
#     print(f"Error during sync invocation (ensure API key is set): {e}")





# --- Asynchronous Invocation

async def get_explanation(topic_dict):
    return await explanation_chain.ainvoke(topic_dict)

async def main_async():
    console.rule("\n[bold blue]--- Asynchronous Invocation ---")
    
    topic_input_async = {"user_topic": "black holes"} 

    try:
        async_explanation = await get_explanation(topic_input_async)
        console.print(Markdown(f"Async Explanation for '{topic_input_async['user_topic']}':\n{async_explanation}"))
    except Exception as e:
        print(f"Error during async invocation (ensure API key is set): {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())


    #     # You can also test the sync part directly if OPENAI_API_KEY is set 
    if os.getenv("OPENAI_API_KEY"): 
        sync_explanation = explanation_chain.invoke({"user_topic": "photosynthesis"})   
        print(f"Explanation for 'photosynthesis':\n{sync_explanation}") 
    else: 
        print("Skipping sync example as API key is not set.") 


