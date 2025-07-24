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
    
async def manual_react_turn():
    console = Console()
    system_prompt_react = """ 
        You are MovieBot, an AI expert on films, designed to answer questions about movies. 
        To do this, you must use the following tools and output format strictly. 
        
        Available Tools: 
        1. `movie_db.find_director(movie_title: str) -> str`: Returns the director's name for a given movie. 
        2. `movie_db.find_release_year(movie_title: str) -> int`: Returns the release year for a given 
        movie. 
        
        Output Format: 
        Thought: [Your reasoning about what to do next, which tool to use, and why. If you have enough 
        information to answer, reason about how to construct the final answer.] 
        Action: [tool_name.method(parameter_name="value") OR FinalAnswer(answer_string="Your 
        final answer here.")] 
        
        After your Action, I will provide an Observation. You will then continue with Thought/Action. 
        Repeat this process until you can provide the FinalAnswer. Only use the tools provided. 
    """ 
    initial_user_question = "Who directed the movie 'Inception' and what year was it released?"

    console.rule("[bold green]--- ReAct Simulation: Turn 1 ---")
    
    messages_turn1: List[Dict[str, str]] = [ 
        {"role": "system", "content": system_prompt_react}, 
        {"role": "user", "content": initial_user_question} 
    ] 

    console.print(Markdown(f"Initial Question: {initial_user_question}"))
    llm_response_turn1_content = await get_llm_response(messages_turn1, temperature=0.0)
    console.print(Markdown(f"From LLM Response:\n{llm_response_turn1_content}"))

    console.rule("[bold green]--- ReAct Simulation: Turn 2 ---")
    observation_director = "Christopher Nolan"
    console.print(Markdown(f"To LLM (User - providing Observation): {observation_director}"))
    messages_turn2 = messages_turn1 + [
        {"role": "assistant", "content": llm_response_turn1_content}, # Add LLM's previous response 
        {"role": "user", "content": f"Observation: {observation_director}"} 
    ]
    llm_response_turn2_content = await get_llm_response(messages_turn2, temperature=0.0)
    console.print(Markdown(f"From LLM Response:\n{llm_response_turn2_content}"))

    console.rule("[bold green]--- ReAct Simulation: Turn 3 ---")
    observation_year = "2010"
    console.print(Markdown(f"To LLM (User - providing Observation): {observation_year}"))
    messages_turn3 = messages_turn2 + [
        {"role": "assistant", "content": llm_response_turn2_content}, # Add LLM's previous response 
        {"role": "user", "content": f"Observation: {observation_year}"}
    ]
    llm_response_turn3_content = await get_llm_response(messages_turn3, temperature=0.0)
    console.print(Markdown(f"From LLM Response:\n{llm_response_turn3_content}"))
    
async def main():
    await manual_react_turn()

if __name__ == "__main__":
    asyncio.run(main())


