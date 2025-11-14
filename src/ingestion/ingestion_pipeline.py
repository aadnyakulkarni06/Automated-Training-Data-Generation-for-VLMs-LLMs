"""
ingestion_pipeline.py
---------------------
This script combines PDF-to-image conversion and OCR extraction
into a single automated pipeline.
"""

import os
from pdf_to_images import pdf_to_images
from ocr_extraction import extract_text_from_images

def process_pdf(pdf_path):
    """
    Complete ingestion pipeline: converts PDF to images, runs OCR,
    and saves text output as JSON.
    """
    if not os.path.exists(pdf_path):
        print(f"[ERROR] File not found: {pdf_path}")
        return
    
    print(f"[INFO] Starting ingestion pipeline for {pdf_path}")
    
    # Step 1: Convert PDF to images
    image_paths = pdf_to_images(pdf_path, output_dir="data/processed/images")
    
    # Step 2: Extract text from generated images
    extract_text_from_images(image_paths, ocr_output_path="data/processed/ocr_output.json")
    
    print("[SUCCESS] Ingestion pipeline completed ✅")


if __name__ == "__main__":
    # Example usage: update the file name here
    sample_pdf = "data/raw/manual.pdf"
    process_pdf(sample_pdf)
