import asyncio
from async_config import client
from rich.console import Console
from rich.markdown import Markdown

async def get_llm_response_few_shot(messages_list: list) -> str: 
    """ 
    Gets a response from the LLM given a list of messages (can include few-shot examples). 
    """ 
    try: 
        response = await client.chat.completions.create( 
            model="gpt-4.1-nano",
            messages=messages_list, 
            temperature=0.3, # Adjust as needed, often lower for style consistency 
        ) 
        return response.choices[0].message.content.strip() 
    except Exception as e: 
        return f"An error occurred: {e}" 
    
async def few_shot_style_transfer_task(): 
    console = Console() 
    system_prompt_style = "You are an expert editor specializing in transforming informal text into formal, professional language. Preserve the core meaning completely. Only output the transformed text." 

    messages = [ 
        {"role": "system", "content": system_prompt_style}, 
        {"role": "user", "content": "Hey, gotta cancel our meeting tomorrow, something came up."}, 
        {"role": "assistant", "content": "I regret to inform you that I must cancel our scheduled meeting for tomorrow due to an unforeseen circumstance. I apologize for any inconvenience this may cause."}, 
        {"role": "user", "content": "Can u send me the report ASAP?"}, 
        {"role": "assistant", "content": "Could you please send me the report at your earliest convenience?"}, 
        {"role": "user", "content": "lol, that bug was a real pain in the neck!"}, # Another example 
        {"role": "assistant", "content": "That particular software defect presented a significant challenge."}, 
        # New query for the LLM to complete 
        {"role": "user", "content": "schedule meeting tomorrow at 2 pm with team"} 
    ] 
    console.rule("[bold blue]--- Few-Shot Style Transfer Task ---") 
    formal_output = await get_llm_response_few_shot(messages) 
    console.print(Markdown((f"Informal Input: schedule meeting tomorrow at 2 pm with team")))
    console.print(Markdown((f"Formal Output: {formal_output}")))

    messages_test_2 = messages[:-1] + [{"role": "user", "content": "its good docs but need improvement by eod"}] 
    console.print(Markdown("\n--- Test 2 ---"))
    formal_output_2 = await get_llm_response_few_shot(messages_test_2) 
    console.print(Markdown((f"Informal Input: its good docs but need improvement by eod")))
    console.print(Markdown((f"Formal Output: {formal_output_2}")))

async def main(): 
    await few_shot_style_transfer_task()

if __name__ == "__main__": 
    asyncio.run(main())