from sentence_transformers import SentenceTransformer

# 1. Load a pre-trained model 
model_name = 'all-MiniLM-L6-v2' 

try:
  model = SentenceTransformer(model_name)
  print(f'Model {model_name} loaded successfully.')
except Exception as e:
  print(f'Error loading model {model_name}: {e}')
  print('Please ensure you have a working internet connection for the first download of the model.')
  exit()

# 2. Define a list of sentences to encode
sentences = [
    "The weather is sunny and warm today.", 
    "It's a beautiful day for a walk in the park.", 
    "I need to buy groceries: milk, eggs, and bread.", 
    "Financial markets reacted to the new inflation report.",
    "I am Umar Fayyaz, AI Engineer."  
]

# Generate embeddings
print("\nGenerating embeddings...")

try:
  embeddings = model.encode(sentences)
except Exception as e:
  print(f'Error generating embeddings: {e}')
  exit()

# 3. Print information about the embeddings
print(f"\nGenerated {len(embeddings)} embeddings.")
for i, sentence in enumerate(sentences):
    print(f"Sentence {sentence}")
    # print the first 5 dimensions of the embedding
    print(f"Embedding shape: {embeddings[i].shape}")

# Example: Embeddings for the first sentence
first_embedding = embeddings[0]
print(f"\nFull embedding for the first sentence: (shape {first_embedding.shape})")

# print(first_embedding) # Potentially very long output 
print(f"\nDimensionality of embeddings: {model.get_sentence_embedding_dimension()}")
print(f"\nMax sequence length for this model: {model.max_seq_length} tokens")
print("\nSuccessfully generated embeddings!")
