from configuration.config import client
from openai import OpenAI, RateLimitError, Timeout, APIError
from typing import List, Dict, Any, Optional
import time

def query_gpt(messages: List[Dict[str, Any]], max_retries: int = 3) -> Optional[Any]:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages,
                timeout=15
            )
            return response
        except RateLimitError as e:
            wait = 2 ** attempt
            print(f"Rate limit exceeded. Retrying in {wait} seconds...")
            time.sleep(wait)
            continue
        except Timeout as e:
            print(f"Request timed out. Retrying...")
            continue
        except APIError as e:
            if e.http_status != 500:
                raise
            print("Server error, retrying...")
            continue
    raise Exception("Failed to get a response after multiple retries.")


messages: List[Dict[str, str]] = [
        {"role": "user", "content": "What's the difference between AI and Generative AI?"}
]

response= query_gpt(messages)
print("Model reply:", response.choices[0].message.content)