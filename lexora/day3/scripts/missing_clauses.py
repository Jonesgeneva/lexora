from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR.parent / "data" / "processed"

# ----------------------------
# Mandatory Clauses (Rule-Based)
# ----------------------------
MANDATORY_CLAUSES = {
    "confidentiality": ["confidential", "non-disclosure"],
    "termination": ["terminate", "termination", "notice"],
    "payment": ["salary", "payment", "compensation"],
    "working_hours": ["working hours", "work hours", "timings"],
    "leave_policy": ["leave", "paid leave", "casual leave"]
}

# ----------------------------
# Process each document
# ----------------------------
for doc_file in PROCESSED_DIR.glob("*.txt"):

    print("\n" + "=" * 70)
    print(f"📄 Document: {doc_file.name}")
    print("=" * 70)

    with open(doc_file, "r", encoding="utf-8") as f:
        text = f.read().lower()

    missing = []

    for clause, keywords in MANDATORY_CLAUSES.items():
        if not any(keyword in text for keyword in keywords):
            missing.append(clause.replace("_", " ").title())

    if missing:
        print("⚠️ Missing Clauses:")
        for m in missing:
            print(f"❌ {m}")
    else:
        print("✅ All mandatory clauses present")
