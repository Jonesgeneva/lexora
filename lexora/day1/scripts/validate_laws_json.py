# scripts/validate_laws_json.py
import json, os, sys
from jsonschema import validate, Draft7Validator

SCHEMA = {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "section": {"type": "string"},
      "title": {"type": "string"},
      "raw_text": {"type": "string"},
      "easy_meaning": {"type": "string"},
      "punishment": {"type": "string"},
      "example": {"type": "string"},
      "related_sections": {"type": "array"}
    },
    "required": ["section", "title", "raw_text"]
  }
}

def validate_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    v = Draft7Validator(SCHEMA)
    errors = sorted(v.iter_errors(data), key=lambda e: e.path)
    if errors:
        print("Found errors:")
        for e in errors:
            print(e)
        return False
    print("Validation OK:", path)
    return True

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "..", "data", "laws", "laws.json")
    if not os.path.exists(path):
        print("laws.json not found at", path)
        sys.exit(1)
    validate_file(path)
