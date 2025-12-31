import json
from pathlib import Path
from transformers import pipeline

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
INPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "processed"

# ----------------------------
# Load Summarization Model
# ----------------------------
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# ----------------------------
# Summarize Clauses
# ----------------------------
def summarize_clauses(clauses):
    summarized = []

    for clause in clauses:
        text = clause["text"]

        # Skip very small text
        if len(text.split()) < 30:
            summary = text
        else:
            result = summarizer(
                text,
                max_length=120,
                min_length=40,
                do_sample=False
            )
            summary = result[0]["summary_text"]

        summarized.append({
            "clause_id": clause["clause_id"],
            "summary": summary
        })

    return summarized

# ----------------------------
# Process Files
# ----------------------------
def process_files():
    clause_files = list(INPUT_DIR.glob("*_clauses.json"))

    for file in clause_files:
        with open(file, "r", encoding="utf-8") as f:
            clauses = json.load(f)

        summaries = summarize_clauses(clauses)

        output_file = OUTPUT_DIR / f"{file.stem}_summary.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summaries, f, indent=2)

        print(f"✅ Summary created: {output_file.name}")

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    process_files()
