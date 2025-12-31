from transformers import pipeline
from src.config import QA_MODEL

class AnswerExtractor:
    def __init__(self):
        self.qa_pipeline = pipeline(
            "question-answering",
            model=QA_MODEL
        )

    def extract(self, question, context):
        result = self.qa_pipeline(
            question=question,
            context=context
        )
        return result["answer"], result["score"]
