import fitz  # PyMuPDF
import re
import os
import json
import faiss
from sentence_transformers import SentenceTransformer

if __name__ == "__main__":
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

    # Track current weather and country
    current_weather = ""
    current_country = ""
    section_buffer = []

    print(f"--->>>Processing {len(doc)} pages from PDF...")

    for page in doc:
        lines = page.get_text().split('\n')

        for line in lines:
            line = line.strip()

            # Detect weather headers like "1. Sunny Weather"
            if re.match(r'^\d+\.\s+(Sunny|Rainy|Snowy|Windy|Cloudy)\s+Weather', line):
                if section_buffer:
                    # Save the previous section before changing
                    joined_text = " ".join(section_buffer).strip()
                    full_context = f"{current_country}, {current_weather}:\n{joined_text}"
                    chunks.append(full_context)
                    metadata.append({
                        "country": current_country,
                        "weather": current_weather,
                        "text": full_context
                    })
                    section_buffer = []

                current_weather = line
                continue

            # Detect country like "USA (California):"
            if re.match(r'^[A-Z][a-zA-Z0-9\s\-\'\.()]+:$', line):
                if section_buffer:
                    # Save previous section
                    joined_text = " ".join(section_buffer).strip()
                    full_context = f"{current_country}, {current_weather}:\n{joined_text}"
                    chunks.append(full_context)
                    metadata.append({
                        "country": current_country,
                        "weather": current_weather,
                        "text": full_context
                    })
                    section_buffer = []

                current_country = line.replace(":", "").strip()
                continue

            # Add normal content
            if current_country and current_weather and line:
                section_buffer.append(line)

    # Save any final buffer at the end
    if section_buffer:
        joined_text = " ".join(section_buffer).strip()
        full_context = f"{current_country}, {current_weather}:\n{joined_text}"
        chunks.append(full_context)
        metadata.append({
            "country": current_country,
            "weather": current_weather,
            "text": full_context
        })

    print(f"--->>>Collected {len(chunks)} full content chunks.")

    # === Generate Embeddings ===
    print("--->>> Generating embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    # === Create FAISS Index ===
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # === Save Index and Metadata ===
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


