import asyncio
from async_config import client
from rich.console import Console
from rich.markdown import Markdown
from typing import List, Dict, Any

async def get_llm_response(prompt_messages: list, temperature: float = 0.2) -> str: 
    try: 
        response = await client.chat.completions.create( 
            model="gpt-4.1-nano",  
            messages=prompt_messages, 
            temperature=temperature, 
        ) 
        return response.choices[0].message.content.strip() 
    except Exception as e: 
        return f"An error occurred: {e}" 
    
async def zero_shot_cot_task()->str:
    console = Console()
    user_question:str = """ 
        Q: Natalia sold clips to 48 of her friends and then divided the clips into 9 equal boxes. 
        If Natalia sold 2 clips to each friend, how many clips are in each box? 
        Let's think step by step. 
        """ 
    system_prompt_cot:str = "You are a meticulous math problem solver. When asked a question, first provide a step-by-step derivation of your thought process, and then state the final answer clearly prefixed with 'The final answer is '." 
    user_prompt_explicit_cot:str = """ 
    Natalia sold clips to 48 of her friends and then divided the clips into 9 equal boxes. 
    If Natalia sold 2 clips to each friend, how many clips are in each box? 
    Please show your reasoning. 
    """ 
    messages: List[Dict[str, str]] = [ 
        {"role": "system", "content": system_prompt_cot}, 
        {"role": "user", "content": user_question} 
    ] 
    console.rule("[bold green]--- Zero-Shot CoT Task ---")
    response_cot = await get_llm_response(messages)
    console.print(Markdown(f"LLM Response: {response_cot}"))

async def main():
    await zero_shot_cot_task()

if __name__ == "__main__":
    asyncio.run(main())