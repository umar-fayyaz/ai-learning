from configuration.config import client

response = client.chat.completions.create( 
    model="gpt-4.1-nano-2025-04-14",  # specify the model 
    messages=[{"role": "user", "content": "What’s the capital of France?"}], 
    max_tokens=50,    
    # cap the response length to 50 tokens 
    temperature=0.7   # a moderate level of creativity 
) 
answer = response.choices[0].message.content 
print("Model reply:", answer)
