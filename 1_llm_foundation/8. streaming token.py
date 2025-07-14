from configuration.config import client
import sys

try:
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": "difference between ai and generative ai"}],
        temperature=0.5,
        top_p=0.5,
        max_tokens=200,
        stream=True
    )
    print("Streaming response:")

    for chunk in response:
        if chunk.choices[0].delta and chunk.choices[0].delta.content:
            sys.stdout.write(chunk.choices[0].delta.content)
            sys.stdout.flush()
except Exception as e:
    print(f'An exception occurred: {e}')