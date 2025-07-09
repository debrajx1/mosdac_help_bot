# vectorstore/semantic_search.py

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model and FAISS index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vectorstore/faiss_index.bin")

# Load mapping of index to content
with open("vectorstore/id_to_text.pkl", "rb") as f:
    id_to_text = pickle.load(f)

# Semantic search with section prioritization and distance threshold
def semantic_search(query, top_k=5, distance_threshold=1.0, return_top_only=True):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for dist, idx in zip(distances[0], indices[0]):
        if idx not in id_to_text:
            continue

        entry = id_to_text[idx]
        section = entry.get("section", "")
        source_type = entry.get("source_type", "unknown")

        # Boost priority for important sections
        boost = 1.0
        if section.lower() in ["introduction", "overview", "mission overview", "insat-3dr"]:
            boost = 0.8  # Prioritize by reducing distance

        adjusted_distance = dist * boost

        if adjusted_distance < distance_threshold:
            results.append({
                "text": entry["text"],
                "source": entry["source"],
                "section": section,
                "source_type": source_type,
                "adjusted_distance": adjusted_distance
            })

    # Sort by best match
    results = sorted(results, key=lambda x: x["adjusted_distance"])

    # Optionally return only the best match
    if return_top_only:
        if results:
            return [results[0]]
        else:
            return []

    # Remove adjusted_distance before returning
    for r in results:
        r.pop("adjusted_distance", None)

    return results
