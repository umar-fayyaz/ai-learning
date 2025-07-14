from configuration.config import client
from typing import List, Dict, Any

function_def:List[Dict[str,str]] = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
]

messages: List[Dict[str,str]] = [
    {"role": "user", "content": "What is ai?"}
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    functions=function_def,
    function_call="auto",
)

message: Dict[str, Any] = response.choices[0].message
print(message)

if message.function_call:
    print("\n Model chose to call a function:")
    print("Function name:", message.function_call.name)
    print("Arguments:", message.function_call.arguments)
else:
    print("\nGPT Model Reply:", message.content)