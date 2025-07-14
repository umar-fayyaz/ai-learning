from openai import OpenAI, RateLimitError
from configuration.config import client
import time
import sys

for attempt in range(5):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": "difference between ai and generative ai"}],
            temperature=0.5,
            top_p=0.5,
            max_tokens=100,
            stream=True
        )
        print("Response received successfully:")
        for chunk in response:
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                sys.stdout.write(chunk.choices[0].delta.content)
                sys.stdout.flush()
        break
    except RateLimitError as e:
        wait = 2 ** attempt
        print(f"Rate limit exceeded. Retrying in {wait} seconds...")
        time.sleep(wait)
else:
    print("Failed after multiple retries due to rate limits")