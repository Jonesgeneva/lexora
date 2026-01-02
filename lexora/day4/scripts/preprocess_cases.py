import json
import re
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

RAW_FILE = DATA_DIR / "cases_raw" / "cases.json"
OUT_FILE = DATA_DIR / "cases_processed" / "cases_ml.json"

# -----------------------------
# Text Cleaning
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -----------------------------
# Load raw cases
# -----------------------------
with open(RAW_FILE, "r", encoding="utf-8") as f:
    cases = json.load(f)

processed = []

for case in cases:
    facts = clean_text(case["facts"])

    charges = " ".join(
        clean_text(ch) for ch in case.get("charges", [])
    )

    full_text = f"{facts} {charges}".strip()

    label = 1 if case["outcome"].lower() == "convicted" else 0

    processed.append({
        "text": full_text,
        "label": label
    })

# -----------------------------
# Save processed data
# -----------------------------
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2)

print(f"✅ Preprocessed {len(processed)} cases")
print(f"📁 Saved to: {OUT_FILE}")
