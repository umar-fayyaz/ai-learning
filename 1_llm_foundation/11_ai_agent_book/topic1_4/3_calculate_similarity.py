from sentence_transformers import SentenceTransformer 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances 

# 1. Load a model and get some embeddings (reusing from Mini-Task 1) 
model = SentenceTransformer('all-MiniLM-L6-v2') 
sentences = [ 
    "The cat sits on the mat.", 
    "A feline is resting upon the rug.", # Semantically similar to sentence 1 
    "It is raining heavily today.",      
    # Different topic 
    "What is the current weather like?" # A question, related to sentence 3 
]

print("Generating embeddings...") 
embeddings = model.encode(sentences) 
print(f"Embeddings shape: {embeddings.shape}") # Should be (4, 384)

# Our query embedding will be the first sentence 
query_embedding = embeddings[0] 
corpus_embeddings = embeddings[1:] # The other sentences 

# Reshape query_embedding to be a 2D array for scikit-learn functions 
query_embedding_2d = query_embedding.reshape(1, -1) 

# 2. Calculate Cosine Similarity 
# sklearn.metrics.pairwise.cosine_similarity expects 2D arrays 
cos_sim_scores = cosine_similarity(query_embedding_2d, corpus_embeddings) 
print("\nCosine Similarity Scores (Query vs Corpus):") 

# cos_sim_scores is a 2D array like [[score1, score2, score3]] 
for i, score in enumerate(cos_sim_scores[0]):
    print(f"  Query vs Sentence {i+2} ('{sentences[i+1]}'): {score:.4f}")

# 3. Calculate Euclidean Distance 
# Lower distance means more similar 
euclidean_dist_scores = euclidean_distances(query_embedding_2d, corpus_embeddings) 
print("\nEuclidean Distances (Query vs Corpus):") 
for i, dist in enumerate(euclidean_dist_scores[0]): 
    print(f"  Query vs Sentence {i+2} ('{sentences[i+1]}'): {dist:.4f}")

# 4. Calculate Dot Product (Manual for illustration, assuming normalization) 
# Note: all-MiniLM-L6-v2 produces normalized embeddings. 
# So, dot product should be very close to cosine similarity here. 
print("\nDot Product Scores (Query vs Corpus - assuming normalized embeddings):") 
for i, doc_embedding in enumerate(corpus_embeddings): 
    dot_product_score = np.dot(query_embedding, doc_embedding) 
    print(f"  Query vs Sentence {i+2} ('{sentences[i+1]}'): {dot_product_score:.4f}")

# Pro Tip: Normalizing embeddings before dot product or L2 distance 
# If you weren't sure if embeddings are normalized: 
# query_norm = query_embedding / np.linalg.norm(query_embedding) 
# corpus_norms = [emb / np.linalg.norm(emb) for emb in corpus_embeddings] 
# dot_product_normalized = np.dot(query_norm, corpus_norms[0]) # Example for first corpus item 
# print(f"\nDot product with explicitly normalized first corpus item: {dot_product_normalized:.4f}")

query_norm = query_embedding / np.linalg.norm(query_embedding)
corpus_norms = [emb / np.linalg.norm(emb) for emb in corpus_embeddings]

print("\nDot Product with Explicit Normalization (same as cosine similarity):")
for i, norm_emb in enumerate(corpus_norms):
    dot_product_normalized = np.dot(query_norm, norm_emb)
    print(f"  Query vs Sentence {i+2} ('{sentences[i+1]}'): {dot_product_normalized:.4f}")

