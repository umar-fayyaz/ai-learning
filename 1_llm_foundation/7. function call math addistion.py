from configuration.config import client
import json 
from typing import List, Dict, Any

function_defs: List[Dict[str, Any]] = [
    {
        "name": "add_numbers",
        "description": "Add two numbers and return the result.",
      "parameters": { 
        "type": "object", 
        "properties": { 
            "a": {"type": "number", "description": "First number"}, 
            "b": {"type": "number", "description": "Second number"} 
        }, 
        "required": ["a", "b"] 
      } 
    } 
] 

messages: List[Dict[str, str]] = [{"role": "user", "content": "What is 26 + 14? Please just give the number."}] 

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    functions=function_defs,
    function_call="auto"
    )

assistant_message: Dict[str, Any] = response.choices[0].message
if assistant_message.function_call:
    func_name:str = assistant_message.function_call.name
    args_json:str = assistant_message.function_call.arguments
    if func_name == "add_numbers":
        result:int = args_json["a"] + args_json["b"]
        messages.append(assistant_message)
        messages.append({
            "role": "function",
            "name": func_name,
            "content": json.dumps({"result": result})
        })

        follow_up = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages
        )
        final_reply:str = follow_up.choices[0].message.content
        print("\nAssistant Final Answer:\n", final_reply)
