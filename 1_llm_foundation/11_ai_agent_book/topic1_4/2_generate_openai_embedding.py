# import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

try:
  client = OpenAI()
  client.models.list()
except:
  print("Error initializing OpenAi client or authenticating: {e}")
  print("Please ensure you have set the OPENAI_API_KEY environment variable.")
  exit()

model_id = 'text-embedding-3-small'

texts_to_embed = [
    "The quick brown fox jumps over the lazy dog.", 
    "Exploring the capabilities of AI embeddings.", 
    "Hivemind: Building the future of AI agents." 
]

print(f"Requesting embeddings for {len(texts_to_embed)} texts...")

try:
  response = client.embeddings.create(input=texts_to_embed, model=model_id)
  all_embeddings = []
  for i, emb_object in enumerate(response.data):
    print(f"Text: \"{texts_to_embed[i]}\"")
    print(f"Embedding vector length: {len(emb_object.embedding)}")
    all_embeddings.append(emb_object.embedding)
    print("-" * 20)

    print(f"\nModel used: {response.model}")
    print(f"Total tokens used: {response.usage.total_tokens}")
    print(f"Prompt tokens used: {response.usage.prompt_tokens}")

except Exception as e:
  print(f"An error occured: {e}")