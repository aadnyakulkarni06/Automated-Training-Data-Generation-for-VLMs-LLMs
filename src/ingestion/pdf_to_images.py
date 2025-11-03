from pathlib import Path
from pdf2image import convert_from_path


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 200):
    """Convert a PDF into images (one per page).

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory where images will be saved.
        dpi: Image resolution.
    Returns:
        List of saved image paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi)
    saved = []
    for i, img in enumerate(images, start=1):
        out = output_dir / f"page_{i:03}.png"
        img.save(out, "PNG")
        saved.append(str(out))
    return saved
