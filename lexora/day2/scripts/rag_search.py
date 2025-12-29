import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# ----------------------------
# Paths (robust)
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
EMBED_DIR = DATA_DIR / "embeddings"

LAW_FILE = DATA_DIR / "laws.json"
INDEX_FILE = EMBED_DIR / "laws.index"

# ----------------------------
# Load model & data
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

with open(LAW_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

laws = data["sections"]

index = faiss.read_index(str(INDEX_FILE))

# ----------------------------
# Semantic Search Function
# ----------------------------
def search(query, top_k=5):
    """
    Semantic retrieval using embeddings (not keywords)
    """
    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    ).reshape(1, -1)

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        law = laws[idx]
        results.append({
            "rank": rank + 1,
            "section": law["section"],
            "title": law["title"],
            "description": law["description"],
            "score": float(distances[0][rank])
        })

    return results

# ----------------------------
# CLI Entry Point
# ----------------------------
if __name__ == "__main__":
    print("\n🧠 IPC RAG Search Engine")
    print("Type your legal question (or 'exit')\n")

    while True:
        query = input("❓ Ask a legal question: ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        results = search(query)

        print("\n🔍 Top Relevant IPC Sections:\n")

        for r in results:
            print("=" * 60)
            print(f"Section : {r['section']}")
            print(f"Title   : {r['title']}")
            print(f"Text    : {r['description']}")
            print("=" * 60)
