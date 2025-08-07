from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.console import Console
from rich.markdown import Markdown
import asyncio


from dotenv import load_dotenv
load_dotenv()
console = Console()

chat_model = ChatOpenAI(model="gpt-4.1-nano",temperature=0)

string_parser = StrOutputParser()

prompt_template = ChatPromptTemplate.from_template("Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner. (Answer must be in markdown format & bullet points)")

chain = (
    RunnablePassthrough() 
    | prompt_template 
    | chat_model 
    | string_parser
)


async def main():

    console.rule("\n[bold blue]--- Welcome to Chatbot ---")
    console.print(Markdown("Enter the Topic Name: "))
    topic_input = console.input()
    try:
        result = await chain.ainvoke({"user_topic": topic_input})
        
        console.print(Markdown(f"Explanation for '{topic_input}':\n\n{result}"))
    except Exception as e:
        print(f"Error during async invocation (ensure API key is set): {e}")


if __name__ == "__main__":
    asyncio.run(main())