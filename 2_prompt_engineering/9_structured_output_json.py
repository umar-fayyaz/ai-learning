import asyncio
import os
import json
from async_config import client
from rich.console import Console
from rich.markdown import Markdown

async def get_json_output_task()->str:
    system_prompt_json = ( 
        "You are an AI assistant that extracts product information from text" 
        "and outputs it as a valid JSON object. The JSON object MUST contain exactly two keys: " 
        "'product_name' (string) and 'price' (float)." 
    )

    user_prompt_product = "The new 'UltraWidget X100' is now available for only $49.99!" 

    console = Console()
    console.rule("[bold green]--- JSON Output Task (with JSON Mode) ---")
    try:
        response = await client.chat.completions.create(
         
        model = "gpt-4.1-nano",
        messages = [
            {"role": "system", "content": system_prompt_json},
            {"role": "user", "content": user_prompt_product}
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
        )
        raw_json_output = response.choices[0].message.content
        console.print(Markdown(f"Raw LLM Output: {raw_json_output}"))

        try:
            parsed_json = json.loads(raw_json_output)
            console.print(Markdown(f"Parsed JSON Output: \n{parsed_json}"))
            if 'product_name' in parsed_json and 'price' in parsed_json:
                console.print(Markdown("\nJSON contains the required keys"))
            else:
                console.print(Markdown("\nJSON does not contain the required keys"))
        except json.JSONDecodeError as e:
            console.print(Markdown(f"\nError: Output was not valid JSON: {e}"))

    except Exception as e:
        print(f'An API error occured: {e}')

async def main():
    await get_json_output_task()

if __name__ == "__main__":
    asyncio.run(main())