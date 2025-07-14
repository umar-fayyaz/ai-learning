from configuration.config import client

prompt = "Give one creative analogy to explain the concept of artificial intelligence."

for temp in [0.0, 1.0]:
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=temp
    )
    print(f"Temperature: {temp}: {response.choices[0].message.content}")