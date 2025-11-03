# Setup Instructions

1. Create and activate a Python virtual environment (recommended):

   python3 -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. Install Tesseract OCR on macOS:

   brew install tesseract

4. (Optional) Install poppler for pdf2image:

   brew install poppler

5. Run tests:

   pytest -q
