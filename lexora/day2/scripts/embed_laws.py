import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# ----------------------------
# Paths (robust & OS-safe)
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
EMBED_DIR = DATA_DIR / "embeddings"

LAW_FILE = DATA_DIR / "laws.json"
INDEX_FILE = EMBED_DIR / "laws.index"

EMBED_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Load embedding model
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# Load laws.json
# ----------------------------
with open(LAW_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

sections = data["sections"]

print(f"📚 Total IPC Sections Loaded: {len(sections)}")

# ----------------------------
# Prepare text for embedding
# ----------------------------
texts = []
for law in sections:
    combined_text = (
        f"Section {law['section']}. "
        f"{law['title']}. "
        f"{law['description']}"
    )
    texts.append(combined_text)

# ----------------------------
# Generate embeddings
# ----------------------------
embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

# ----------------------------
# Build FAISS index
# ----------------------------
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, str(INDEX_FILE))

print(f"✅ FAISS index created")
print(f"📦 Total vectors indexed: {index.ntotal}")
print(f"📁 Saved to: {INDEX_FILE}")
