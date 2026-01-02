from src.ingestion.ingestion_pipeline import process_pdf
from src.annotation.pipeline import run_annotation_and_qa
from src.utils.file_utils import get_latest_cleaned_file

def run(uploaded_file=None, cleaned_json_path=None):
    if uploaded_file:
        ingestion_outputs = process_pdf(uploaded_file)
        cleaned_path = ingestion_outputs["cleaned"]

    elif cleaned_json_path:
        cleaned_path = cleaned_json_path
        ingestion_outputs = {}

    else:
        cleaned_path = get_latest_cleaned_file()
        ingestion_outputs = {}

    qa_outputs = run_annotation_and_qa(
        cleaned_json_path=cleaned_path
    )

    return {
        **ingestion_outputs,
        **qa_outputs
    }