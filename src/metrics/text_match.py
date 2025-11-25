import json
from collections import Counter

def normalize_text(text):
    """Normalize text for comparison"""
    text = text.lower()
    text = text.replace('"', "'").replace('"', "'").replace('"', "'")
    text = text.replace(''', "'").replace(''', "'")
    text = text.replace('©', '').replace('€', '')
    return text

def get_words(text):
    """Extract words from text"""
    normalized = normalize_text(text)
    words = [word.strip() for word in normalized.split() if word.strip()]
    return words

def analyze_ocr_from_file(json_file_path, original_text_file_path):
    """
    Analyze OCR text from JSON file
    
    Args:
        json_file_path: Path to JSON file containing OCR data
        original_text_file_path: Path to text file with original PDF text
    """
    
    # Read original text
    try:
        with open(original_text_file_path, 'r', encoding='utf-8') as f:
            original_text = f.read()
    except UnicodeDecodeError:
        with open(original_text_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            original_text = f.read()
    
    # Read OCR JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        ocr_data = json.load(f)
    
    print("=" * 80)
    print("PDF OCR TEXT ANALYSIS")
    print("=" * 80)
    print()
    
    # Get original words
    original_words = get_words(original_text)
    original_word_set = set(original_words)
    
    print(f"Total words in original PDF: {len(original_words)}")
    print()
    
    # Analyze each page
    print("-" * 80)
    print("WORD COUNT BY PAGE")
    print("-" * 80)
    
    all_extracted_words = []
    
    # Iterate through JSON array
    for page in ocr_data:
        page_num = page['page_number']
        clean_text = page['clean_text']
        words = get_words(clean_text)
        word_count = len(words)
        
        all_extracted_words.extend(words)
        
        print(f"Page {page_num}: {word_count} words")
        print(f"Preview: {clean_text[:100]}...")
        print()
    
    print(f"Total extracted words: {len(all_extracted_words)}")
    print()
    
    # Find missing words
    extracted_word_set = set(all_extracted_words)
    missing_words = [word for word in original_words if word not in extracted_word_set]
    
    # Get unique missing words with counts
    missing_word_counts = Counter(missing_words)
    unique_missing_words = sorted(missing_word_counts.keys())
    
    print("-" * 80)
    print("MISSING WORDS ANALYSIS")
    print("-" * 80)
    print(f"Total missing word occurrences: {len(missing_words)}")
    print(f"Unique missing words: {len(unique_missing_words)}")
    print()
    
    if unique_missing_words:
        print("Missing words (with occurrence count):")
        print()
        for word in unique_missing_words:
            count = missing_word_counts[word]
            print(f"  '{word}' - appears {count} time(s)")
    else:
        print("No missing words found!")
    
    print()
    print("-" * 80)
    print("SUMMARY")
    print("-" * 80)
    accuracy = ((len(original_words) - len(missing_words)) / len(original_words)) * 100
    print(f"OCR Accuracy: {accuracy:.2f}%")
    print(f"Words correctly extracted: {len(original_words) - len(missing_words)}")
    print(f"Words missing: {len(missing_words)}")
    print("=" * 80)

# Example usage
if __name__ == "__main__":
    # Specify your file paths
    json_file = "data/cleaned/cleaned_text.json"  # Your JSON file with OCR data
    original_file = "data/raw/manual.pdf"  # Your original PDF text
    
    analyze_ocr_from_file(json_file, original_file)