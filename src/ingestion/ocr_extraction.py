from PIL import Image
import pytesseract
from pathlib import Path


def image_to_text(image_path: str, lang: str = 'eng') -> str:
    """Run OCR on an image and return extracted text."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text
