import fitz  # PyMuPDF
import re
import os
import json
import faiss
from sentence_transformers import SentenceTransformer

# === File Paths ===
PDF_PATH = "Weather Activity Clothing Database.pdf"
INDEX_PATH = "vector_store/faiss_index.bin"
METADATA_PATH = "vector_store/chunk_metadata.json"

# === Prepare output directories ===
os.makedirs("vector_store", exist_ok=True)

# === Load Embedding Model ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Open PDF ===
doc = fitz.open(PDF_PATH)
chunks = []
metadata = []

# === Track current weather section and country ===
current_weather = ""
current_country = ""

print(f"Processing {len(doc)} pages in the PDF...")

for page in doc:
    lines = page.get_text().split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Detect weather section headers like "1. Sunny Weather"
        if re.match(r'^\d+\.\s+(Sunny|Rainy|Snowy|Windy)\s+Weather', line):
            current_weather = line
            continue

        # Detect country names like "USA (California):"
        if re.match(r'^[A-Z][a-zA-Z0-9\s\-\'\.()]+:$', line):
            current_country = line.replace(":", "").strip()
            continue

        # Add full labeled context for semantic clarity (bonus tip)
        if current_country and current_weather:
            text_with_context = f"{current_country}, {current_weather}:\n{line}"
            chunks.append(text_with_context)
            metadata.append({
                "country": current_country,
                "weather": current_weather,
                "preview": line[:100] + "..."
            })

print(f"--->>Collected {len(chunks)} valid chunks for embedding.")

# === Generate Embeddings ===
print("---->>Generating embeddings...")
embeddings = model.encode(chunks, show_progress_bar=True)

# === Create FAISS Index ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === Save Index and Metadata ===
faiss.write_index(index, INDEX_PATH)
with open(METADATA_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("--->>FAISS index and metadata saved successfully.")
