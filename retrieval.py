import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Paths
INDEX_PATH = "vector_store/faiss_index.bin"
METADATA_PATH = "vector_store/chunk_metadata.json"

# Load index, metadata, and embedding model
print("--->>Loading index and metadata...")
index = faiss.read_index(INDEX_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_chunks(query, top_k=3):
    """
    Takes a user query, searches FAISS for the top_k matching chunks.
    Returns: List of (chunk text, metadata)
    """
    query_embedding = model.encode([query])
    query_vector = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_vector, top_k)
    print("---->>Indices returned:", indices)


    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            result = {
                "text": metadata[idx]["text"],  # now the full chunk!
                "metadata": {
                    "country": metadata[idx]["country"],
                    "weather": metadata[idx]["weather"]
                }
            }
            results.append(result)
    print(f"Found {len(results)} results for query: '{query}'")
    return results

            

