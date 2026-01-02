import os
from src.ingestion.pdf_to_images import pdf_to_images
from src.ingestion.ocr_extraction import extract_text_from_images
from src.cleaning.text_cleaner import clean_json


# Ensure folders exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed/images", exist_ok=True)
os.makedirs("data/cleaned", exist_ok=True)


def process_pdf(uploaded_file):
    # Base filename
    base_name = uploaded_file.name.rsplit(".", 1)[0]

    # Save uploaded PDF
    pdf_path = f"data/raw/{uploaded_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: PDF → Images
    image_paths = pdf_to_images(
        pdf_path,
        output_dir="data/processed/images"
    )

    # Step 2: OCR Extraction
    ocr_output_path = f"data/processed/{base_name}_ocr.json"
    extract_text_from_images(
        image_paths=image_paths,
        ocr_output_path=ocr_output_path
    )

    # Step 3: Cleaning OCR Text
    cleaned_output_path = f"data/cleaned/{base_name}_cleaned.json"
    clean_json(
        input_path=ocr_output_path,
        output_path=cleaned_output_path
    )

    # Return ONLY ingestion outputs
    return {
        "ocr": ocr_output_path,
        "cleaned": cleaned_output_path
    }
