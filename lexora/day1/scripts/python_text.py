# scripts/pdf_to_text.py
import os
import sys
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from tqdm import tqdm
import argparse

def python_text(pdf_path, out_txt_path, dpi=300, poppler_path=None):
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    full_text = []
    for img in tqdm(images, desc=f"OCR pages of {os.path.basename(pdf_path)}"):
        text = pytesseract.image_to_string(img, lang='eng')
        full_text.append(text)
    with open(out_txt_path, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(full_text))
    return out_txt_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Path to PDF file")
    parser.add_argument("--output", "-o", default=None, help="Path to output .txt")
    parser.add_argument("--poppler_path", default=None, help="POPPLER path (Windows)")
    args = parser.parse_args()
    input_pdf = args.input
    out = args.output or os.path.splitext(os.path.basename(input_pdf))[0] + ".txt"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(BASE_DIR, "data", "texts", out)if not os.path.isabs(out) else out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    python_text(input_pdf, out_path, poppler_path=args.poppler_path)
    print("ABSOLUTE OUTPUT PATH:", os.path.abspath(out_path))
    print("Saved:", out_path)
