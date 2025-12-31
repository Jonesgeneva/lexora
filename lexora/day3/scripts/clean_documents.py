import re
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

INPUT_DIR = DATA_DIR / "documents"
OUTPUT_DIR = DATA_DIR / "processed"

OUTPUT_DIR.mkdir(exist_ok=True)

# ----------------------------
# Text Cleaning Function
# ----------------------------
def clean_text(text: str) -> str:
    """
    Clean legal document text safely
    """

    # Remove page numbers (lines with only numbers)
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    # Remove non-ASCII symbols (keep legal text clean)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Restore paragraph structure
    text = text.replace(" .", ".").replace(" ,", ",")

    return text.strip()

# ----------------------------
# Process All Documents
# ----------------------------
def process_documents():
    txt_files = list(INPUT_DIR.glob("*.txt"))

    if not txt_files:
        print("❌ No text files found in documents folder")
        return

    print(f"📄 Found {len(txt_files)} documents")

    for file in txt_files:
        with open(file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned_text = clean_text(raw_text)

        output_file = OUTPUT_DIR / file.name
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"✅ Cleaned: {file.name}")

    print("\n🎯 All documents cleaned successfully")

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    process_documents()
