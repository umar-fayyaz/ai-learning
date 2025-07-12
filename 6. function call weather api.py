from config import client


import json
from datetime import date
from rich import print
from rich.console import Console
from rich.markdown import Markdown

console = Console()

function_def = {
    "name": "get_weather",
    "description": "Get the weather forecast for a given city and day",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"},
            "date": {"type": "string", "description": "Date in YYYY-MM-DD"}
        },
        "required": ["city", "date"]
    }
}

messages = [
    {"role": "user", "content": "What is weather today in Lahore? provide your final output in markdown"}
]

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    functions=[function_def],
    function_call="auto"
)

response_msg = response.choices[0].message
if response_msg.function_call:
    print("\nModel triggered function call")
    func_name = response_msg.function_call.name
    args_json = response_msg.function_call.arguments
    args = json.loads(args_json)  # Convert JSON string to dict
    print("Function Name:", func_name)
    print("Arguments:", args)
    # Step 7: Simulate weather API call
    def call_fake_weather_api(city, date):
        return {
            "location": city,
            "date": date,
            "forecast": "Sunny with a high of 27°C and a low of 18°C"
        }
    # Call fake weather API with extracted arguments
    result = call_fake_weather_api(**args)
    # Step 8: Append function result to messages
    messages.append({
        "role": "function",
        "name": func_name,
        "content": json.dumps(result)
    })
    # Step 9: Ask GPT to respond using the function result
    follow_up = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages
    )
    final_reply = follow_up.choices[0].message.content
    console.print("\nAssistant Final Answer :\n", Markdown(final_reply))

else:
    print("\nNo function call. Model answered directly:")
    console.print(Markdown(response_msg.content))