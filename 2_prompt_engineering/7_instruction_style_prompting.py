import asyncio
from async_config import client
from rich.console import Console
from rich.markdown import Markdown
from typing import List, Dict

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
    

async def instruction_style_prompting()->str:
    console = Console()
    messages_instruction_style: List[Dict[str, str]] = [ 
        { 
            "role": "system", 
            "content": "You are 'SummaryBot', an AI skilled in extracting key information and summarizing technical documents for a non-technical audience. Your summaries should be concise, in bullet points, and under 150 words." 
        }, 
        { 
            "role": "user", 
            "content": """ 
            Please summarize the following research paper abstract. 
            Focus on the main objective, method, and key findings. 
            Abstract Title: "The Impact of Quantum Entanglement on Data Transmission Speeds" 
            Abstract Text: 
            "Recent advancements in quantum physics have opened new avenues for revolutionizing data 
            communication. This paper investigates the potential of leveraging quantum entanglement to 
            achieve faster-than-light (FTL) data transmission, a concept previously confined to theoretical 
            speculation. We propose a novel experimental setup involving entangled particle pairs 
            generated via spontaneous parametric down-conversion. One particle of each pair is modulated 
            based on the input data stream, while its entangled counterpart, located at a distant receiver, 
            instantaneously reflects this modulation. Our preliminary results indicate a statistically significant 
            correlation in state changes across distances up to 10 kilometers, with transmission latencies 
            independent of this distance. While challenges related to decoherence and scalable particle 
            generation persist, these findings suggest a foundational step towards practical FTL 
            communication systems, potentially transforming global networking and deep-space 
            communication." 
            Ensure your summary is clear and avoids heavy jargon. 
            """ 
        }
    ] 
    console.rule("[bold blue]--- Instruction Style Prompting ---") 
    response_output = await get_llm_response_few_shot(messages_instruction_style) 
    console.print(Markdown((f"Summary: {response_output}")))

async def main():
    await instruction_style_prompting()

if __name__ == "__main__":
    asyncio.run(main())
