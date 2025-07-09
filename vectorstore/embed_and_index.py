# vectorstore/embed_and_index.py

import json
import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# File paths
STATIC_JSON = "data/static_pages/parsed_static_pages.json"
DOCS_JSON = "data/parsed_docs.json"
INDEX_FILE = "vectorstore/faiss_index.bin"
MAPPING_FILE = "vectorstore/id_to_text.pkl"

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Helper to chunk text
def chunk_text(text, chunk_size=10000):
    sentences = text.split('. ')
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= chunk_size:
            chunk += sentence + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + ". "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

corpus = []
id_to_text = {}
idx = 0

# === 1. Embed static .txt-based JSON ===
if os.path.exists(STATIC_JSON):
    with open(STATIC_JSON, "r", encoding="utf-8") as f:
        static_data = json.load(f)

    for doc_name, sections in static_data.items():
        for section, content in sections.items():
            chunks = chunk_text(content)
            for chunk in chunks:
                corpus.append(chunk)
                id_to_text[idx] = {
                    "text": chunk,
                    "source": doc_name,
                    "section": section,
                    "source_type": "static"
                }
                idx += 1

# === 2. Embed PDF/DOCX/XLSX documents ===
if os.path.exists(DOCS_JSON):
    with open(DOCS_JSON, "r", encoding="utf-8") as f:
        docs_data = json.load(f)

    for doc_name, full_text in docs_data.items():
        chunks = chunk_text(full_text)
        for chunk in chunks:
            corpus.append(chunk)
            id_to_text[idx] = {
                "text": chunk,
                "source": doc_name,
                "section": "full_document",
                "source_type": "docs"
            }
            idx += 1

# === 3. Embedding & Indexing ===
print("🔍 Embedding all data...")
embeddings = model.encode(corpus, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and mapping
faiss.write_index(index, INDEX_FILE)
with open(MAPPING_FILE, "wb") as f:
    pickle.dump(id_to_text, f)

print("✅ FAISS index and mapping saved.")
print(f"🧠 Total chunks embedded: {len(corpus)}")
