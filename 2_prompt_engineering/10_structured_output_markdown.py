import asyncio
import json
from async_config import client
from rich.console import Console
from rich.markdown import Markdown
from typing import List, Dict, Any

async def get_markdown_output_task()->str:
    system_prompt_markdown = (
        "You are an AI assistant that extracts product information from text "
        "and outputs it in **Markdown** format. Format it as follows:\n\n"
        "**Product Name:** <product name>\n"
        "**Price:** $<price>\n"
    )

    user_prompt_product:str = "The new 'UltraWidget X100' is now available for only $49.99!" 

    console = Console()
    console.rule("[bold cyan]--- Markdown Output Task ---")
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt_markdown},
                {"role": "user", "content": user_prompt_product}
            ],
            temperature=0.1,
            # No response_format here to allow flexible Markdown output
        )
        markdown_output = response.choices[0].message.content
        console.print(Markdown(markdown_output))

    except Exception as e:
        console.print(f'[red]An API error occurred: {e}')

async def main():
    await get_markdown_output_task()

if __name__ == "__main__":
    asyncio.run(main())
