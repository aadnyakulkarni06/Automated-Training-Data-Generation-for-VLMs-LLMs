"""
text_cleaner.py
---------------
Cleans OCR-extracted text by removing unwanted symbols, extra spaces,
and formatting issues.
"""

import json
import re
import os

def clean_text(text):
    # Remove weird symbols, multiple spaces, and control chars
    text = re.sub(r'\s+', ' ', text)  # normalize spaces
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # remove non-ASCII
    text = text.strip()
    return text

def clean_json(input_path="data/processed/ocr_output.json",
               output_path="data/cleaned/cleaned_text.json"):
    with open(input_path, "r") as f:
        data = json.load(f)

    for entry in data:
        entry["clean_text"] = clean_text(entry["text"])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[INFO] Cleaned text saved to {output_path}")

if __name__ == "__main__":
    clean_json()
