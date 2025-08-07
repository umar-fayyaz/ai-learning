import os
import asyncio
from async_config import client
from typing import List, Dict, Any
from rich import print
from rich.console import Console
from rich.markdown import Markdown
# from rich.rule import Rule

async def get_llm_response(system_message_content:str | None, user_message_content: str) -> str:
    """"
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
    
async def main():
    console = Console()
    user_question = "Tell me about the challenges faced during the late Roman Republic."

    console.rule("[bold red]---Response WITHOUT detailed system persona---")
    response_generic = await get_llm_response(
        system_message_content="You are a helpful assistant.",
        user_message_content=user_question
    )
    console.print(Markdown(response_generic))

    console.rule("\n\n[bold red]---Response WITH detailed system persona: Expert Roman Historian---")
    expert_persona = ( 
        "You are Dr. Livius, an esteemed Professor of Ancient History at Oxford University, " 
        "specializing in the socio-political dynamics of the late Roman Republic. " 
        "Your explanations are detailed, nuanced, and draw upon primary historical sources where appropriate, " 
        "but are articulated for an intelligent layperson. You avoid overly simplistic narratives." 
    ) 

    response_expert = await get_llm_response(
        system_message_content=expert_persona,
        user_message_content=user_question
    )
    console.print(Markdown(response_expert))

if __name__ == "__main__":
    asyncio.run(main())