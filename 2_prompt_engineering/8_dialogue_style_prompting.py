import asyncio
from async_config import client
from rich.console import Console
from rich.markdown import Markdown
from typing import List, Dict

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
    messages_dialogue_style:List[Dict[str, str]] = [ 
        {"role": "system", "content": "You are a helpful brainstorming assistant for marketing slogans. Final output in markdown format."}, 
        {"role": "user", "content": "Suggest three slogans for a new brand of eco-friendly coffee."} 
    ]

    console.rule("[bold blue]--- Dialogue Style Prompting ---")
    assistant_response_1 = await get_llm_response_few_shot(messages_dialogue_style)
    console.print(Markdown((f"Slogan 1: {assistant_response_1}")))

    # Followup
    console.print(Markdown("\n--- Followup ---"))
    messages_dialogue_style.append({"role": "assistant", "content": assistant_response_1}) 
    messages_dialogue_style.append({"role": "user", "content": "I like the first one. Can you make it punchier and highlight the 'freshness' aspect?"}) 
    assistant_response_2 = await get_llm_response_few_shot(messages_dialogue_style)
    console.print(Markdown((f"Slogan 2: {assistant_response_2}")))

async def main():
    await dialogue_style_prompting()

if __name__ == "__main__":
    asyncio.run(main())