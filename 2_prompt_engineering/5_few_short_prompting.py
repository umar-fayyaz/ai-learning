import asyncio
from async_config import client
from rich.console import Console
from rich.markdown import Markdown

async def get_llm_response(messages: list[dict]) -> str:
    """
    Get a response from the LLM given a full message history (few-shot style).
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

async def few_shot_classification():
    console = Console()

    system_prompt = """You are an AI assistant that categorizes fruit names by their typical color. 
Possible colors are: Red, Yellow, Green, Orange, Purple. 
Output only the color.
Fruit: Apple 
Color: Red 
### 
Fruit: Banana 
Color: Yellow 
### 
Fruit: Lime 
Color: Green
"""

    # Few-shot message history + final query
    messages = [ 
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": "Grape"}, 
        # {"role": "assistant", "content": "Red"}, 
        # {"role": "user", "content": "Banana"}, 
        # {"role": "assistant", "content": "Yellow"}, 
        # {"role": "user", "content": "Lime"}, 
        # {"role": "assistant", "content": "Green"}, 
        # {"role": "user", "content": "Grape"}  # Final query
    ]

    console.rule("[bold green]Few-Shot Classification Example")
    result = await get_llm_response(messages)
    console.print(Markdown(f"**Grape** → Classified as: `{result}`"))

async def main():
    await few_shot_classification()

if __name__ == "__main__":
    asyncio.run(main())
