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
    
async def zero_shot_classification_task():
    console = Console()
    system_message = (
        "You are 'SupportAI-Classifier', an expert AI assistant. " 
        "Your task is to classify the following customer query into one of these exact categories: " 
        "'Billing Inquiry', 'Technical Issue', 'Feature Request', 'Account Cancellation', 'Change of Subscription'." 
        "Output only the category name and nothing else." 
    )
    queries = {
        "q1": "My payment didn't go through, can you check?", 
        "q2": "The app crashes every time I click the 'export' button.", 
        "q3": "It would be great if you could add a dark mode to the interface.", 
        "q4": "How do I close my account and get a refund for the remaining period?", # Touches on cancellation and billing 
        "q5": "The website is slow today when I try to log in.", 
        "q6": "I want to upgrade my subscription plan." # Potentially 'Billing Inquiry' or a new category 
    }

    console.rule("[bold yellow]--- Zero-Shot Classification Task ---")
    
    for q_id, query_text in queries.items():
        classification = await get_llm_response(system_message,query_text)
        console.print(Markdown(f"Query ({q_id}): \"{query_text}\" -> Classified as: {classification}"))

async def main():
    await zero_shot_classification_task()

if __name__ == "__main__":
    asyncio.run(main())
