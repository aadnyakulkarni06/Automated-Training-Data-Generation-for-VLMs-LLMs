from .pdf_to_images import pdf_to_images
from .ocr_extraction import image_to_text


def ingest_pdf(pdf_path: str, workspace_dir: str):
    images = pdf_to_images(pdf_path, f"{workspace_dir}/data/raw/images")
    ocr_texts = []
    for img in images:
        ocr_texts.append(image_to_text(img))
    return images, ocr_texts
