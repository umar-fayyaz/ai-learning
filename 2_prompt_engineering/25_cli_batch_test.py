import asyncio 
import json 
import time 
from async_config import client
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def load_prompt_variants(filepath="2_prompt_engineering/25_cli_batch_test_data_result/prompt_variants.json"):
    """Loads prompt variants from a JSON file."""

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"Error: Prompt variants file '{filepath}' not found.")
        return {}

    except json.JSONDecodeError:
        console.print(f"Error: Invalid JSON format in '{filepath}'.")
        return {}
    
def load_test_cases(filepath="2_prompt_engineering/25_cli_batch_test_data_result/test_cases.json"):
    """Loads test cases from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"Error: Test cases file '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        console.print(f"Error: Invalid JSON format in '{filepath}'.")
        return []
    
async def run_experiment(prompt_variant_name, system_prompt, user_prompt_template, test_case, temperature, model_name = "gpt-4.1-nano"):
    """ 
    Runs a single experiment for one prompt variant and one test case. 
    """ 
    if isinstance (test_case, dict):
        try:
            user_prompt = user_prompt_template.format(**test_case) 
        except KeyError as e:
            console.print(f"Error: Missing Key {e} in test_case for prompt formatting. Test case: {test_case}")
            return None
    else:
        user_prompt = user_prompt_template.format(input=test_case)
    
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    start_time = time.perf_counter()

    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
        )
        latency = time.perf_counter() - start_time
        llm_response = response.choices[0].message.content
        usage = response.usage

        result = {
            "prompt_variant_name": prompt_variant_name, 
            "system_prompt": system_prompt, 
            "user_prompt": user_prompt, # Log the formatted user prompt 
            "test_case_input": test_case, 
            "temperature": temperature, 
            "model_name": model_name, 
            "llm_response": llm_response, 
            "latency_seconds": round(latency, 4), 
            "prompt_tokens": usage.prompt_tokens if usage else None, 
            "completion_tokens": usage.completion_tokens if usage else None, 
            "total_tokens": usage.total_tokens if usage else None, 
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S") 
        }
        return result
    except Exception as e:
        console.print(f"Error during API call for {prompt_variant_name} with test case '{test_case}': {e}")
        latency = time.perf_counter() - start_time
        return None
    
async def main_batch_runner():
    prompt_variants = load_prompt_variants() # Expects a dict: {"variant_name": {"system": "...", "user_template": "..."}} 
    test_cases = load_test_cases() # Expects a list of inputs, e.g., ["input1", "input2"] or [{"query": "q1", "context": "c1"}] 

    all_results = []

    temperatures_to_test = [0.2, 0.5, 0.8, 1.2]

    for variant_name, prompt_data in prompt_variants.items():
        system_prompt = prompt_data.get("system", "")
        user_p_template = prompt_data.get("user_template", "{input}")

        for test_case in test_cases:
            for temperature in temperatures_to_test:
                console.print(f"Running: {variant_name} - Test Case: {str(test_case)[:50]} - Temperature: {temperature}")
                result = await run_experiment(variant_name, system_prompt, user_p_template, test_case, temperature)
                if result:
                    all_results.append(result)
                    console.print(Markdown(f" LLM Output: {str(result['llm_response'])[:100]}"))
                    console.print(Markdown(f" Latency: {result['latency_seconds']:.2f} s, Tokens: {result['total_tokens']}"))

    output_file = "2_prompt_engineering/25_cli_batch_test_data_result/experiment_result.jsonl"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    console.print(f"\nAll experiments complete. Results saved to {output_file}.")

if __name__ == "__main__":
    dummy_prompts = { 
        "variant_A_formal": { 
            "system": "You are a formal summarizer.", 
            "user_template": "Please formally summarize the following text: {input}" 
    }, 
        "variant_B_bullet": { 
            "system": "You are a concise summarizer that uses bullet points.", 
            "user_template": "Summarize this text using bullet points: {input}" 
    },
        "variant_C_casual": {
            "system": "You are a casual, friendly summarizer.",
            "user_template": "Hey! Can you break this down in a simple and friendly way? {input}"
    },
        "variant_D_translate": {
            "system": "You are a French translator.",
            "user_template": "Translate this into French: {input}"
    }
}


    with open("2_prompt_engineering/25_cli_batch_test_data_result/prompt_variants.json", "w") as f: 
        json.dump(dummy_prompts, f, indent=2)


    dummy_test_cases = [ 
        "The quick brown fox jumps over the lazy dog. This sentence is famous for containing all letters of the English alphabet.", 
        "Large language models are transforming various industries by automating tasks, generating creative content, and providing insights from data.",
        "Climate change is accelerating due to increased greenhouse gas emissions from human activities, especially fossil fuel burning.",
        "Space exploration has advanced significantly with reusable rockets, allowing more frequent and cost-effective missions to orbit and beyond."
]


    with open("2_prompt_engineering/25_cli_batch_test_data_result/test_cases.json", "w") as f: 
        json.dump(dummy_test_cases, f, indent=2) 
 
    asyncio.run(main_batch_runner()) 