from .image_captioning import generate_image_captions
from .qa_generation import generate_qa_from_texts


def annotate(images, texts):
    captions = generate_image_captions(images)
    qa = generate_qa_from_texts(texts)
    return {"captions": captions, "qa": qa}
