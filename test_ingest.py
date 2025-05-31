import json
import faiss
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import json

if __name__ == "__main__":
    # === Load metadata ===
    with open("vector_store/chunk_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print("✅ Number of chunks:", len(metadata))

    # === Load FAISS index ===
    index = faiss.read_index("vector_store/faiss_index.bin")

    # === Check number of vectors stored ===
    print("--->>> Number of vectors stored:", index.ntotal)

    # === Reconstruct all vectors from index ===
    vectors = index.reconstruct_n(0, index.ntotal)
    print("--->>> Vector matrix shape:", vectors.shape)  # Should be (n_chunks, embedding_dim)
    print("--->>> First vector sample:", vectors[0])  # Print first vector for sanity check
    print("--->>> First metadata sample:", metadata[0])  # Print first metadata for sanity check

#


