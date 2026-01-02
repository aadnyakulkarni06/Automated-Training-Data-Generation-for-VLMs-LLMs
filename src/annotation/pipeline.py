import os
from src.annotation.qa_pipeline import QAPipeline
from src.annotation.annotation_pipeline import annotate_json


def run_annotation_and_qa(cleaned_json_path):
    """
    Takes cleaned OCR JSON and produces:
    1. Annotated JSON
    2. QA dataset JSON
    """

    base_name = os.path.basename(cleaned_json_path).replace("_cleaned.json", "")

    # -----------------------------
    # Ensure folders
    # -----------------------------
    os.makedirs("data/annotated", exist_ok=True)
    os.makedirs("data/final", exist_ok=True)

    # -----------------------------
    # Step 4: NLP Annotation
    # -----------------------------
    annotated_output_path = f"data/annotated/{base_name}_annotated.json"

    annotate_json(
        input_path=cleaned_json_path,
        output_path=annotated_output_path
    )

    # -----------------------------
    # Step 5: QA Generation
    # -----------------------------
    qa_output_path = f"data/final/{base_name}_qa.json"

    qa_pipeline = QAPipeline()
    qa_pipeline.process(
        input_path=annotated_output_path,
        output_path=qa_output_path
    )

    return {
        "annotated": annotated_output_path,
        "qa": qa_output_path
    }