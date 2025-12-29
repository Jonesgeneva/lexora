import faiss
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "..", "data", "embeddings", "laws.index")

index = faiss.read_index(INDEX_PATH)
print("Total vectors in index:", index.ntotal)

