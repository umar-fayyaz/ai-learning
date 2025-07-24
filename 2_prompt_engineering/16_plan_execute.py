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

async def plan_generation_task()->str:
    console = Console()
    system_prompt_planner = ( 
        "You are 'ProjectPlannerAI', an expert AI assistant skilled at breaking down " 
        "software development projects into clear, manageable, and actionable steps. " 
        "The plans should be high-level but cover the essential phases." 
    ) 
    user_prompt_todo_app = """ 
        I want to build a simple command-line To-Do list application in Python. 
        Please generate a 4-step plan for creating this application. The plan should cover: 
        1. Defining the core features and task structure. 
        2. Deciding on a simple data storage mechanism (e.g., JSON or CSV file). 
        3. Implementing basic CRUD (Create, Read, Update, Delete) operations for tasks. 
        4. Designing and implementing the command-line interface for user interaction. 
 
        Output the plan as a numbered list, with each step briefly described. 
    """ 
    messages = [ 
        {"role": "system", "content": system_prompt_planner}, 
        {"role": "user", "content": user_prompt_todo_app} 
    ] 

    console.rule("[bold green]--- Plan Generation Task (To Do App)---")
    response = await get_llm_response(messages,temperature=0.3)
    console.print(Markdown(f"Generated Plan: \n{response}"))

async def main():
    await plan_generation_task()

if __name__ == "__main__":
    asyncio.run(main())