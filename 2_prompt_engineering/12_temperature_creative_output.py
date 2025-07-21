import asyncio
from async_config import client
from rich.console import Console
from rich.markdown import Markdown
from typing import List, Dict

async def get_llm_response_with_temp(messages_list: list, temperature: float) -> str: 
    try: 
        response = await client.chat.completions.create( 
            model="gpt-4o", 
            messages=messages_list, 
            temperature=temperature, 
        ) 
        return response.choices[0].message.content.strip() 
    except Exception as e: 
        return f"An error occurred: {e}" 
    
async def temperature_experiment_task()->str:
    console = Console()
    system_prompt_story:str = "You are a fantasy storyteller with a vivid imagination, known for your unique creature descriptions."
    user_prompt_creature = ( 
        "Describe a newly discovered creature called a 'Shadow Whisperer'. " 
        "Focus on its appearance, habitat, and one unique ability. Keep the description under 75 words." 
    ) 
    messages: List[Dict[str, str]] = [ 
        {"role": "system", "content": system_prompt_story}, 
        {"role": "user", "content": user_prompt_creature} 
    ]

    console.rule("\n[bold green]--- Temperature Experiment Task ---")

    temp_low: float = 0.2

    console.rule(f"[bold yellow]Output with Temperature: {temp_low}")
    response_low_temp = await get_llm_response_with_temp(messages, temp_low)
    console.print(Markdown(response_low_temp))

    temp_medium:float = 0.7
    console.rule(f"[bold red]Output with Temperature: {temp_medium}")
    response_medium_temp = await get_llm_response_with_temp(messages, temp_medium)
    console.print(Markdown(response_medium_temp))

    temp_high:float = 1.2
    console.rule(f"[bold blue]Output with Temperature: {temp_high}")
    response_high_temp = await get_llm_response_with_temp(messages, temp_high)
    console.print(Markdown(response_high_temp))

async def main():
    await temperature_experiment_task()

if __name__ == "__main__":
    asyncio.run(main())