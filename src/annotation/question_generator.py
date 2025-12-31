from transformers import T5Tokenizer, T5ForConditionalGeneration
from src.config import QG_MODEL

class QuestionGenerator:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained(QG_MODEL)
        self.model = T5ForConditionalGeneration.from_pretrained(QG_MODEL)

    def generate(self, context):
        input_text = "generate question: " + context
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True
        )

        outputs = self.model.generate(
            **inputs,
            max_length=64,
            num_beams=4
        )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
