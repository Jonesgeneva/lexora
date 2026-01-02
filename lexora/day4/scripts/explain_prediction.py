import joblib
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

# Day 4 (ML)
MODEL_DIR = BASE_DIR.parent / "models"
VECTORIZER_FILE = MODEL_DIR / "tfidf_vectorizer.pkl"
MODEL_FILE = MODEL_DIR / "case_prediction_model.pkl"

# Day 2 (RAG)
DAY2_DATA = BASE_DIR.parents[1] / "day2" / "data"
LAW_FILE = DAY2_DATA / "laws.json"
INDEX_FILE = DAY2_DATA / "embeddings" / "laws.index"

# -----------------------------
# Load Components
# -----------------------------
vectorizer = joblib.load(VECTORIZER_FILE)
model = joblib.load(MODEL_FILE)

rag_model = SentenceTransformer("all-MiniLM-L6-v2")
rag_index = faiss.read_index(str(INDEX_FILE))

with open(LAW_FILE, "r", encoding="utf-8") as f:
    laws = json.load(f)["sections"]

# -----------------------------
# Explainability Logic (FIXED)
# -----------------------------
def explain_case(text, top_words=5, top_laws=3):

    # ---- ML Reasoning ----
    vec = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    coefs = model.coef_[0]

    scores = vec.toarray()[0] * coefs
    top_indices = np.argsort(scores)[-top_words:][::-1]

    keywords = [feature_names[i] for i in top_indices if scores[i] > 0]

    print("\n🧠 ML Reasoning (Important Words):")
    for w in keywords:
        print(f"  - {w}")

    # ---- RAG Legal Reasoning (FULL TEXT) ----
    print("\n⚖️ Applicable IPC Sections:")

    emb = rag_model.encode(text).reshape(1, -1)
    _, indices = rag_index.search(emb, top_laws * 3)

    shown = 0
    for idx in indices[0]:
        law = laws[idx]

        try:
            sec = int(law["section"])
        except:
            continue

        # Fraud / cheating range
        if 400 <= sec <= 471:
            print(f"  ➤ IPC {law['section']} — {law['title']}")
            shown += 1

        if shown == top_laws:
            break

# -----------------------------
# CLI
# ----------------------------- 
if __name__ == "__main__":
    print("\n🔍 Legal Explainability Engine\n")

    case_text = input("📝 Enter case facts:\n")
    explain_case(case_text)
