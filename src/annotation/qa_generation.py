"""
Generate question-answer pairs from annotations using SBERT.
"""

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

# Question generation templates
def generate_question(annotation):
    sentence_type = annotation["sentence_type"]
    entities = annotation["entities"]
    keywords = annotation["keywords"]

    # Entity-based questions
    for ent in entities:
        if ent["label"] == "DATE":
            return "What year is mentioned?"
        if ent["label"] == "ORG":
            return "Which organization is mentioned?"
        if ent["label"] == "PRODUCT":
            return "Which product is mentioned?"

    # Sentence-type based questions
    if sentence_type == "PROCEDURE":
        return "What procedure is described?"
    if sentence_type == "SAFETY_INSTRUCTION":
        return "What safety instruction is mentioned?"
    if keywords:
        return f"What is {keywords[0]}?"

    return "What information is provided?"

# SBERT helpers
def select_representative(texts):
    """
    Select the most representative text using cosine similarity.
    """
    if len(texts) == 1:
        return texts[0]

    embeddings = model.encode(texts)
    similarity = cosine_similarity(embeddings)
    central_index = np.argmax(similarity.sum(axis=1))

    return texts[central_index]

# Main QA generation function
def generate_qa_pairs(data):
    for entry in data:
        annotation = entry.get("annotations", {})
        text = entry.get("clean_text", "")

        if not annotation or not text:
            entry["qa_pairs"] = []
            continue

        # SBERT operates on sentence-level chunks
        sentences = [text]
        embeddings = model.encode(sentences)

        # Since annotation is page-level, clustering is trivial here
        representative_text = select_representative(sentences)

        question = generate_question(annotation)
        answer = representative_text

        entry["qa_pairs"] = [{
            "question": question,
            "answer": answer
        }]

    return data

# Pipeline function
def run(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        print(f"[ERROR] Annotated file not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = generate_qa_pairs(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[INFO] QA generation completed")
    print(f"[INFO] Output saved to: {output_path}")

# Entry Point
if __name__ == "__main__":
    INPUT_FILE = "data/annotated/manual_annotated.json"
    OUTPUT_FILE = "data/final/qa_dataset.json"

    run(INPUT_FILE, OUTPUT_FILE)