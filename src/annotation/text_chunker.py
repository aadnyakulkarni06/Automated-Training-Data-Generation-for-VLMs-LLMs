import nltk
from nltk.tokenize import sent_tokenize
from src.config import MAX_WORDS_PER_CHUNK

nltk.download("punkt")

def chunk_text(text):
    sentences = sent_tokenize(text)
    chunks, current_chunk = [], []
    word_count = 0

    for sent in sentences:
        words = sent.split()
        if word_count + len(words) > MAX_WORDS_PER_CHUNK:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0

        current_chunk.append(sent)
        word_count += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
