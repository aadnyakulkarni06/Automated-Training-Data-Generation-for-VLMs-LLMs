from typing import List


def generate_qa_from_texts(texts: List[str]):
    """Simple QA pair generator placeholder."""
    qa = []
    for i, t in enumerate(texts, start=1):
        qa.append({"id": i, "question": f"What is in document {i}?", "answer": t[:200]})
    return qa
