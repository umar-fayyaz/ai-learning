import asyncio 
import time 
from typing import Any, Dict, List, Optional, Union 
from uuid import UUID 
from dotenv import load_dotenv 
from langchain_core.callbacks import AsyncCallbackHandler 
from langchain_core.outputs import LLMResult 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI 
load_dotenv() 

class CompreshensiveMonitorHandler(AsyncCallbackHandler):
    """ 
    A custom callback handler that monitors and logs key aspects of an LLM call. 
    """ 

    def __init__(self):
        self.start_times: Dict[UUID, float] = {} 
        self.metrics = {
            "success": 0, 
            "errors": 0, 
            "total_tokens": 0, 
            "prompt_tokens": 0, 
            "completion_tokens": 0, 
            "total_latency": 0.0 
        }

    async def on_llm_start(self, serialized, prompts, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
        """Log the start of an LLM run and record the start time.""" 
        print(f"--- LLM Start --- \nRun ID: {run_id}")
        print(f"Prompts: {prompts}")
        self.start_times[run_id] = time.monotonic()

    async def on_llm_end(self, response: LLMResult, *, run_id, **kwargs)-> None:
        """Log the end of an LLM run, calculate latency, and update metrics.""" 
        latency = time.monotonic() - self.start_times.pop(run_id, 0)

        token_usage = response.llm_output.get("token_usage", {}) 
        prompt_tokens = token_usage.get("prompt_tokens", 0) 
        completion_tokens = token_usage.get("completion_tokens", 0) 
        total_tokens = token_usage.get("total_tokens", 0) 

        print(f"--- LLM END --- Run ID: {run_id} ---") 
        print(f"LATENCY: {latency:.2f} seconds") 
        print(f"TOKENS: {total_tokens} (Prompt: {prompt_tokens}, Completion: {completion_tokens})") 

          # Update metrics 
        self.metrics["success"] += 1 
        self.metrics["prompt_tokens"] += prompt_tokens 
        self.metrics["completion_tokens"] += completion_tokens 
        self.metrics["total_tokens"] += total_tokens 
        self.metrics["total_latency"] += latency 

    async def on_llm_error(self, error: Exception, *, run_id, **kwargs) -> None:
        """Log an error if the LLM run fails.""" 
        print(f"--- LLM ERROR --- Run ID: {run_id} ---") 
        print(f"Error: {error.__class__.__name__}: {error}") 
        self.start_times.pop(run_id, None) 
        self.metrics["errors"] += 1

    def print_summary(self):
        """Prints a summary of all collected metrics.""" 
        print("\n--- MONITORING SUMMARY ---") 
        print(f"Total Runs: {self.metrics['success'] + self.metrics['errors']}") 
        print(f"Successful Runs: {self.metrics['success']}") 
        print(f"Failed Runs: {self.metrics['errors']}") 

        if self.metrics['success']>0:
            avg_latency = self.metrics['total_latency'] / self.metrics['success'] 
            print(f"Average Latency: {avg_latency:.2f} seconds") 

        print(f"Total Tokens Used: {self.metrics['total_tokens']}") 
        print("--------------------------") 

async def main():
    monitor = CompreshensiveMonitorHandler()

    model = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0.0
    )

    prompt = ChatPromptTemplate.from_template("What are the three main benefits of using {technology}?")

    chain = prompt | model

    await chain.ainvoke({"technology": "AI"}, config={"callbacks": [monitor]})

    try:
        error_model = ChatOpenAI(
            model="gpt-not-existent-model",
            temperature=0.0
        )

        error_chain = prompt | error_model

        await error_chain.ainvoke({"technology": "AI"}, config={"callbacks": [monitor]})

    except Exception as e:
        print(f"Error occurred: {e}")

    monitor.print_summary()
if __name__ == "__main__":
    asyncio.run(main())