import json
from pathlib import Path
import spacy 

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Simple rule-based classifier
def classify_sentence(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["warning", "danger", "must", "should"]):
        return "SAFETY_INSTRUCTION"
    elif any(word in text_lower for word in ["step", "procedure", "install"]):
        return "PROCEDURE"
    else:
        return "DESCRIPTION"


def annotate_json(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        print(f"[ERROR] Cleaned file not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        doc = nlp(entry["clean_text"])

        # Named Entity Recognition
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        # Keyword extraction (nouns & proper nouns)
        keywords = list({
            token.text
            for token in doc
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop
        })

        entry["annotations"] = {
            "entities": entities,
            "keywords": keywords,
            "sentence_type": classify_sentence(entry["clean_text"])
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[INFO] Annotated data saved to: {output_path}")