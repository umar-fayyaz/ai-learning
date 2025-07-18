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

async def recipe_formatting_task() ->str:
    console = Console()
    recipe_text = """
    Simple Guacamole: 
    To make this delicious dip, you'll need 2 ripe avocados, 1/2 small onion (finely chopped),  
    1 lime (juiced), salt to taste, and a pinch of cumin.  
    First, mash the avocados in a bowl. Then, stir in the chopped onion, lime juice, salt, and cumin.  
    Mix well and serve immediately with tortilla chips.
    """

    system_chef_persona = "You are 'Chef Quick-Recipe', an expert at clearly presenting recipe information."

    goal_paragraph = ( 
        "From the following recipe text, please extract the ingredients and the preparation steps. " 
        "Present the ingredients in a short paragraph and the cooking instructions in another paragraph." 
    ) 

    prompt1_user_content = f"Recipe Text: \n{recipe_text}\n\nTask: {goal_paragraph}"
    console.rule("[bold red]---Response with Paragraph Goal---")
    response1 = await get_llm_response(system_chef_persona, prompt1_user_content)
    console.print(Markdown(response1))

    goal_list = (
        "From the following recipe text, please extract the ingredients and the preparation steps. " 
        "Present the ingredients as a bulleted list, including quantities. " 
        "Present the cooking instructions as a numbered list." 
    )
    prompt2_user_content = f"Recipe Text:\n{recipe_text}\n\nTask: {goal_list}"
    console.rule("[bold red]--- Response with List Goal ---")
    response2 = await get_llm_response(system_chef_persona, prompt2_user_content)
    console.print(Markdown(response2))


async def main():
    console = Console()
    console.print("Starting the recipe formatting task...")
    await recipe_formatting_task()
    console.rule("[bold White]--- Recipe formatting task completed ---")

if __name__ == "__main__":
    asyncio.run(main())
