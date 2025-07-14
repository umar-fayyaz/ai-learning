from configuration.config import client
from openai import OpenAIError
from typing import Any

messages: list[Any] = [
    {"role": "system", "content": "You are a world-class travel assistant."},
    {"role": "user", "content": "I want to plan a one-week trip to Japan in April. What itinerary do you suggest?"}
]

try:
  response = client.chat.completions.create(
    model="gpt-4.1-nano-2025-04-14", 
    messages=messages,
    max_tokens=300,
    temperature=0.8,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

except OpenAIError as e:
  print(f"API call failed {e}")

assistant_message = response.choices[0].message.content
print("Assistant reply:\n", assistant_message) 

usage = response.usage 
if usage is not None:
    print(f"\n[Usage] prompt_tokens={usage.prompt_tokens}, completion_tokens={usage.completion_tokens}, total={usage.total_tokens}")
else:
    print("\n[Usage] Token usage data not available.")