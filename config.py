from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# response = client.chat.completions.create( 
#     model="gpt-4.1-nano-2025-04-14",  # specify the model 
#     messages=[{"role": "user", "content": "What’s the capital of France?"}], 
#     max_tokens=50,    
#     # cap the response length to 50 tokens 
#     temperature=0.7   # a moderate level of creativity 
# ) 
# answer = response.choices[0].message.content 
# print("Model reply:", answer)



















# messages: list[Any] = [
#     {"role": "system", "content": "You are a world-class travel assistant."},
#     {"role": "user", "content": "I want to plan a one-week trip to Japan in April. What itinerary do you suggest?"}
# ]

# try:
#   response = client.chat.completions.create(
#     model="gpt-4.1-nano-2025-04-14", 
#     messages=messages,
#     max_tokens=300,
#     temperature=0.8,
#     top_p=1.0,
#     frequency_penalty=0.0,
#     presence_penalty=0.0
# )

# except OpenAIError as e:
#   print(f"API call failed {e}")

# assistant_message = response.choices[0].message.content
# print("Assistant reply:\n", assistant_message) 

# usage = response.usage 
# if usage is not None:
#     print(f"\n[Usage] prompt_tokens={usage.prompt_tokens}, completion_tokens={usage.completion_tokens}, total={usage.total_tokens}")
# else:
#     print("\n[Usage] Token usage data not available.")















# prompt = "Give one creative analogy to explain the concept of artificial intelligence."

# for temp in [0.0, 1.0]:
#     response = client.chat.completions.create(
#         model="gpt-4.1-nano-2025-04-14",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=50,
#         temperature=temp
#     )
#     print(f"Temperature: {temp}: {response.choices[0].message.content}")














# user_query = "Weather in Tokyo tomorrow." 
# prompt = f""" 
# You are a weather bot. Provide a JSON with the weather forecast. 
# The JSON should have two keys: "location" and "forecast". 
# Query: "{user_query}" 
# Answer: 
# """

# response = client.chat.completions.create(
#     model="gpt-4.1-nano-2025-04-14", 
#     messages=[{"role": "user", "content": prompt}],
#     temperature=0.5,  
# )

# print("Model reply:", response.choices[0].message.content)
















# function_def = [
#     {
#         "name": "get_weather",
#         "description": "Get the current weather in a given location",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "The city and state, e.g. San Francisco, CA"
#                 },
#                 "unit": {
#                     "type": "string",
#                     "enum": ["celsius", "fahrenheit"]
#                 }
#             },
#             "required": ["location"]
#         }
#     }
# ]

# messages = [
#     {"role": "user", "content": "What is ai?"}
# ]

# response = client.chat.completions.create(
#     model="gpt-4.1",
#     messages=messages,
#     functions=function_def,
#     function_call="auto",
# )

# message = response.choices[0].message
# print(message)

# if message.function_call:
#     print("\n Model chose to call a function:")
#     print("Function name:", message.function_call.name)
#     print("Arguments:", message.function_call.arguments)
# else:
#     print("\nGPT Model Reply:", message.content)

















# import json
# from datetime import date
# from rich import print
# from rich.console import Console
# from rich.markdown import Markdown

# console = Console()

# function_def = {
#     "name": "get_weather",
#     "description": "Get the weather forecast for a given city and day",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "city": {"type": "string", "description": "City name"},
#             "date": {"type": "string", "description": "Date in YYYY-MM-DD"}
#         },
#         "required": ["city", "date"]
#     }
# }

# messages = [
#     {"role": "user", "content": "What is weather today in Lahore? provide your final output in markdown"}
# ]

# response = client.chat.completions.create(
#     model="gpt-4.1-nano",
#     messages=messages,
#     functions=[function_def],
#     function_call="auto"
# )

# response_msg = response.choices[0].message
# if response_msg.function_call:
#     print("\nModel triggered function call")
#     func_name = response_msg.function_call.name
#     args_json = response_msg.function_call.arguments
#     args = json.loads(args_json)  # Convert JSON string to dict
#     print("Function Name:", func_name)
#     print("Arguments:", args)
#     # Step 7: Simulate weather API call
#     def call_fake_weather_api(city, date):
#         return {
#             "location": city,
#             "date": date,
#             "forecast": "Sunny with a high of 27°C and a low of 18°C"
#         }
#     # Call fake weather API with extracted arguments
#     result = call_fake_weather_api(**args)
#     # Step 8: Append function result to messages
#     messages.append({
#         "role": "function",
#         "name": func_name,
#         "content": json.dumps(result)
#     })
#     # Step 9: Ask GPT to respond using the function result
#     follow_up = client.chat.completions.create(
#         model="gpt-4.1-nano",
#         messages=messages
#     )
#     final_reply = follow_up.choices[0].message.content
#     console.print("\nAssistant Final Answer :\n", Markdown(final_reply))

# else:
#     print("\nNo function call. Model answered directly:")
#     console.print(Markdown(response_msg.content))














# import math, json 
# function_defs = [ 
#     { 
#       "name": "add_numbers", 
#       "description": "Add two numbers and return the result.", 
#       "parameters": { 
#         "type": "object", 
#         "properties": { 
#             "a": {"type": "number", "description": "First number"}, 
#             "b": {"type": "number", "description": "Second number"} 
#         }, 
#         "required": ["a", "b"] 
#       } 
#     } 
# ] 

# messages = [{"role": "user", "content": "What is 26 + 14? Please just give the number."}] 

# response = client.chat.completions.create(
#     model="gpt-4.1-nano",
#     messages=messages,
#     functions=function_defs,
#     function_call="auto"
#     )

# assistant_message = response.choices[0].message
# if assistant_message.function_call:
#     func_name = assistant_message.function_call.name
#     args_json = json.loads(assistant_message.function_call.arguments)
#     if func_name == "add_numbers":
#         result = args_json["a"] + args_json["b"]
#         messages.append(assistant_message)
#         messages.append({
#             "role": "function",
#             "name": func_name,
#             "content": json.dumps({"result": result})
#         })

#         follow_up = client.chat.completions.create(
#             model="gpt-4.1-nano",
#             messages=messages
#         )
#         final_reply = follow_up.choices[0].message.content
#         print("\nAssistant Final Answer:\n", final_reply)















# import sys
# try:
#     response = client.chat.completions.create(
#         model="gpt-4.1-nano",
#         messages=[{"role": "user", "content": "difference between ai and generative ai"}],
#         temperature=0.5,
#         top_p=0.5,
#         max_tokens=200,
#         stream=True
#     )
#     print("Streaming response:")

#     for chunk in response:
#         if chunk.choices[0].delta and chunk.choices[0].delta.content:
#             sys.stdout.write(chunk.choices[0].delta.content)
#             sys.stdout.flush()
# except Exception as e:
#     print(f'An exception occurred: {e}')























# import time
# import sys

# for attempt in range(5):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4.1-nano",
#             messages=[{"role": "user", "content": "difference between ai and generative ai"}],
#             temperature=0.5,
#             top_p=0.5,
#             max_tokens=100,
#             stream=True
#         )
#         print("Response received successfully:")
#         for chunk in response:
#             if chunk.choices[0].delta and chunk.choices[0].delta.content:
#                 sys.stdout.write(chunk.choices[0].delta.content)
#                 sys.stdout.flush()
#         break
#     except RateLimitError as e:
#         wait = 2 ** attempt
#         print(f"Rate limit exceeded. Retrying in {wait} seconds...")
#         time.sleep(wait)
# else:
#     print("Failed after multiple retries due to rate limits")

















# import time

# def query_gpt(messages, max_retries=3):
#     for attempt in range(max_retries):
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4.1-nano",
#                 messages=messages,
#                 timeout=15
#             )
#             return response
#         except RateLimitError as e:
#             wait = 2 ** attempt
#             print(f"Rate limit exceeded. Retrying in {wait} seconds...")
#             time.sleep(wait)
#             continue
#         except Timeout as e:
#             print(f"Request timed out. Retrying...")
#             continue
#         except APIError as e:
#             if e.http_status != 500:
#                 raise
#             print("Server error, retrying...")
#             continue
#     raise Exception("Failed to get a response after multiple retries.")


# messages=[
#         {"role": "user", "content": "What's the difference between AI and Generative AI?"}
# ]

# response= query_gpt(messages)
# print("Model reply:", response.choices[0].message.content)