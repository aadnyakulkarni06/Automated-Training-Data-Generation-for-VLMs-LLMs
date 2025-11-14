"""
ocr_pipeline.py
----------------
This script converts a PDF into images, extracts text using OCR,
and saves the result into a JSON file.

You can later use this as the first step in your dataset pipeline.
"""

# --- Step 1: Import libraries ---
import os
import json
from pdf2image import convert_from_path
import pytesseract
from PIL import Image


# --- Step 2: Function to convert PDF pages to images ---
def pdf_to_images(pdf_path, image_output_dir="data/processed/images"):
    os.makedirs(image_output_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=300)
    image_paths = []

    for i, page in enumerate(pages):
        image_path = os.path.join(image_output_dir, f"page_{i+1}.jpg")
        page.save(image_path, "JPEG")
        image_paths.append(image_path)

    print(f"[INFO] {len(image_paths)} pages saved in {image_output_dir}")
    return image_paths


# Function to extract text from each image
def extract_text_from_images(image_paths, ocr_output_path="data/processed/ocr_output.json"):
    extracted_data = []

    for i, img_path in enumerate(image_paths):
        text = pytesseract.image_to_string(Image.open(img_path))
        extracted_data.append({
            "page_number": i + 1,
            "image_path": img_path,
            "text": text.strip()
        })
        print(f"[INFO] Extracted text from page {i+1}")

    # Save all extracted text in JSON format
    os.makedirs(os.path.dirname(ocr_output_path), exist_ok=True)
    with open(ocr_output_path, "w") as f:
        json.dump(extracted_data, f, indent=2)

    print(f"[INFO] OCR results saved to {ocr_output_path}")

# Main Execution
if __name__ == "__main__":
    # Input PDF path
    pdf_path = "data/raw/manual.pdf"   # replace with your PDF file

    # Convert to images
    image_files = pdf_to_images(pdf_path)

    # Extract text using OCR
    extract_text_from_images(image_files)
