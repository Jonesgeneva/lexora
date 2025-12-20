# scripts/make_laws_json.py
import os, json, re
from glob import glob
from tqdm import tqdm

DATA_TEXT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "texts")
OUT_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "laws", "laws.json")

def parse_section_block(text):
    # Simple heuristic: look for lines like 'Section 420. Cheating.'
    # This is a starter parser and should be adapted to your source formatting.
    entries = []
    # naive split on 'Section' occurrences (improve for real scraping)
    parts = re.split(r'(?i)\nsection\s+|\nsec\.\s*', text)
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # try to extract a section number at start
        m = re.match(r'(?P<section>\d+)\.?\s*(?P<title>.+)', p, re.DOTALL)
        if m:
            section = m.group('section').strip()
            title_line = m.group('title').splitlines()[0].strip()
            body = "\n".join(m.group('title').splitlines()[1:]).strip()
            entries.append({
                "section": section,
                "title": title_line,
                "raw_text": body,
                "easy_meaning": "",
                "punishment": "",
                "example": "",
                "related_sections": []
            })
    return entries

def build_laws_json():
    all_entries = []
    files = glob(os.path.join(DATA_TEXT_DIR, "*.txt"))
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            txt = fh.read()
        parsed = parse_section_block(txt)
        if parsed:
            all_entries.extend(parsed)
    # If no sections found, fallback: store file as single entry
    if not all_entries:
        for f in files:
            with open(f, 'r', encoding='utf-8') as fh:
                txt = fh.read()
            all_entries.append({
                "section": os.path.splitext(os.path.basename(f))[0],
                "title": os.path.splitext(os.path.basename(f))[0],
                "raw_text": txt,
                "easy_meaning": "",
                "punishment": "",
                "example": "",
                "related_sections": []
            })
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, 'w', encoding='utf-8') as out:
        json.dump(all_entries, out, indent=2, ensure_ascii=False)
    print("Saved laws.json with", len(all_entries), "entries to", OUT_JSON)

if __name__ == "__main__":
    build_laws_json()
