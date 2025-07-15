import faiss
from sentence_transformers import SentenceTransformer
from typing import List,Any
# import torch
import numpy as np

corpus: List[str] = [
    "Our company offers a comprehensive healthcare plan for all full-time employees.", 
    "Employees are entitled to 20 paid vacation days per year.", 
    "The new software update includes enhanced security features and a revamped user interface.", 
    "Quarterly financial reports indicate a 15% growth in revenue.", 
    "For technical support, please email support@examplecorp.com or call our helpline.", 
    "The healthcare benefits package covers medical, dental, and vision insurance.",
    "To request time off, submit a form through the employee portal at least two weeks in advance.",
    "Security protocols have been upgraded across all company platforms following the recent patch.",
    "Our customer service team is available 24/7 to assist with any issues."
]

query: str = "Tell me about the latest system upgrade."

# Load model
model_name: str = 'all-MiniLM-L6-v2'
print(f"Loading embedding model: {model_name}")
model: SentenceTransformer = SentenceTransformer(model_name)
print("Model loaded successfully.")

# Embedding corpus and query
print("Embedding corpus...")
corpus_embeddings = model.encode(corpus, convert_to_tensor=False)

print("Embedding query...")
query_embedding = model.encode(query, convert_to_tensor=False)

# Convert to NumPy arrays for FAISS (float32)
corpus_embeddings_np = np.array(corpus_embeddings).astype('float32')
query_embedding_np = np.array(query_embedding).astype('float32')

if query_embedding_np.ndim == 1:
    query_embedding_np = query_embedding_np.reshape(1, -1)

# Build FAISS index
print("\n--- Using FAISS for retrieval ---")
dimension: int = corpus_embeddings_np.shape[1]
index = faiss.IndexFlatIP(dimension)  # For cosine similarity
print(f"FAISS index type: {'Inner Product' if isinstance(index, faiss.IndexFlatIP) else 'L2 Distance'}")

# Add to index
index.add(corpus_embeddings_np)
print(f"Number of vectors in FAISS index: {index.ntotal}")

# Search
k_faiss: int = 3
distances, faiss_indices = index.search(query_embedding_np, k_faiss)

# Results
print(f"\nQuery: \"{query}\"")
print(f"\nTop {k_faiss} most similar sentences from FAISS:")
for i in range(k_faiss):
    doc_index = faiss_indices[0][i]
    score = distances[0][i]
    print(f"  {i+1}. \"{corpus[doc_index]}\" (Score: {score:.4f})")
