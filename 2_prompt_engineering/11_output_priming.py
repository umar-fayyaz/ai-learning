import asyncio
from async_config import client
from rich.console import Console
from rich.markdown import Markdown
from typing import List, Dict, Any

async def get_llm_response_few_shot(messages_list: list) -> str: 
    """ 
    Gets a response from the LLM given a list of messages (can include few-shot examples). 
    """ 
    try: 
        response = await client.chat.completions.create( 
            model="gpt-4.1-nano",
            messages=messages_list, 
            # temperature=0.3, # Adjust as needed, often lower for style consistency 
        ) 
        return response.choices[0].message.content.strip() 
    except Exception as e: 
        return f"An error occurred: {e}" 
    
async def dialogue_style_prompting()->str:
    console = Console()
    messages: List[Dict[str, str]] = [ 
        {"role": "system", "content": "You are a poet."}, 
        {"role": "user", "content": "Write a short, melancholic line about autumn leaves."}, 
        {"role": "assistant", "content": "The golden leaves fall, like tears..."} ,# You provide this start 
        {"role": "user", "content": "Complete the lines"}
    ] 
    console.rule("[bold blue]--- Dialogue Style Prompting ---") 
    assistant_response_1 = await get_llm_response_few_shot(messages) 
    console.print(Markdown((f"Slogan: {assistant_response_1}")))

async def main():
    await dialogue_style_prompting()

if __name__ == "__main__":
    asyncio.run(main())