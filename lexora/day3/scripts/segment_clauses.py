import re
import json
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
INPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "processed"

# ----------------------------
# Clause Segmentation Logic
# ----------------------------
def segment_clauses(text: str):
    """
    Split legal text into clauses using numbering & keywords
    """

    # Split on numbered clauses (1., 1.1, (a), etc.)
    raw_clauses = re.split(
        r"\n(?=\d+\.|\([a-z]\)|[A-Z][A-Za-z ]{3,}:)",
        text
    )

    clauses = []
    for i, clause in enumerate(raw_clauses):
        cleaned = clause.strip()
        if len(cleaned) > 50:  # ignore junk
            clauses.append({
                "clause_id": i + 1,
                "text": cleaned
            })

    return clauses

# ----------------------------
# Process All Documents
# ----------------------------
def process_files():
    txt_files = list(INPUT_DIR.glob("*.txt"))

    for file in txt_files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        clauses = segment_clauses(text)

        output_file = OUTPUT_DIR / f"{file.stem}_clauses.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(clauses, f, indent=2)

        print(f"✅ Clauses extracted: {output_file.name}")

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    process_files()
