from configuration.config import client


user_query:str = "Weather in Tokyo tomorrow." 
prompt:str = f""" 
You are a weather bot. Provide a JSON with the weather forecast. 
The JSON should have two keys: "location" and "forecast". 
Query: "{user_query}" 
Answer: 
"""

response = client.chat.completions.create(
    model="gpt-4.1-nano-2025-04-14", 
    messages=[{"role": "user", "content": prompt}],
    temperature=0.5,  
)

print("Model reply:", response.choices[0].message.content)