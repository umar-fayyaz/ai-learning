import asyncio
from async_config import client
from typing import List, Dict
from rich import print
from rich.console import Console
from rich.markdown import Markdown

async def get_llm_response(system_message_content:str | None, user_message_content: str) -> str:
    """
    Get a response from the LLM given system and user messages.Uses gpt-4.1-nano
    """

    message: List[Dict[str, str]] = []
    if system_message_content:
        message.append({"role": "system", "content": system_message_content})
    message.append({"role": "user", "content": user_message_content})
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=message,
            temperature=0.7,
            # max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An Error occured: {e}"


async def conceptual_tool_call():
    console = Console()
    system_message_toll_persona: str = """
        You are 'CalcMate', a helpful shopping assistant. You are great at breaking down cost 
        calculation problems. 
        You have access to the following tool: 
        Tool Name: `calculator` 
        Description: Evaluates a mathematical expression string and returns a numerical result. 
        Usage: `calculator.calculate(mathematical_expression: str) -> number` 
        
        When you need to use the calculator to determine a numerical result as part of your reasoning, 
        you MUST state your intention to use it and the exact expression you would use. 
        Format this as: 
        ACTION: calculator.calculate(mathematical_expression='<your mathematical expression string 
        here>') 
        Do not perform the final calculation yourself in the thought process. Just show the ACTION call. 
        After showing the ACTION, you can then state what the next step would be (e.g., "Then I would 
        present this total to the user."). 
        """ 
    user_message_for_tool:str = (
        "I want to buy 3 t-shirts that cost $20 each and one pair of shorts that cost $40. " 
        "Can you tell me the steps to figure out the total cost and show me how you'd use the calculator for the math part?  (answer must be in markdown format)"
    )

    console.rule("[bold green]--- Conceptual Tool Call Task Response ---")
    response = await get_llm_response(system_message_toll_persona, user_message_for_tool)
    console.print(Markdown(response))

async def main():
    await conceptual_tool_call()

if __name__ == "__main__":
    asyncio.run(main())
