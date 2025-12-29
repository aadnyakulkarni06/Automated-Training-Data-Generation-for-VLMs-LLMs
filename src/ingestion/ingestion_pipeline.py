# src/ingestion/ingestion_pipeline.py

import os
from ingestion.pdf_to_images import pdf_to_images
from ingestion.ocr_extraction import extract_text_from_images
from cleaning.text_cleaner import clean_json
from annotation.text_annotator import annotate_json


# Ensure folders exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed/images", exist_ok=True)
os.makedirs("data/cleaned", exist_ok=True)


def process_pdf(uploaded_file):
    # Save uploaded file to raw folder
    pdf_path = f"data/raw/{uploaded_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: PDF → Images
    image_output_dir = "data/processed/images"
    image_paths = pdf_to_images(pdf_path, output_dir=image_output_dir)

    # Step 2: OCR Extraction
    ocr_output_path = f"data/processed/{uploaded_file.name.split('.')[0]}_ocr.json"
    extract_text_from_images(image_paths, ocr_output_path=ocr_output_path)

    # Step 3: Cleaning OCR Text
    cleaned_output_path = f"data/cleaned/{uploaded_file.name.split('.')[0]}_cleaned.json"
    clean_json(input_path=ocr_output_path, output_path=cleaned_output_path)

    
    # Step 4: NLP Annotation
    annotated_output_path = f"data/annotated/{uploaded_file.name.split('.')[0]}_annotated.json"
    annotate_json(
    input_path=cleaned_output_path,
    output_path=annotated_output_path)

    return annotated_output_path