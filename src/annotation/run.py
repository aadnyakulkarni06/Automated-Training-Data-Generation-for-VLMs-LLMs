from src.annotation.qa_pipeline import QAPipeline

def main():
    pipeline = QAPipeline()
    pipeline.process(
        input_path="data/cleaned/macbook-air-13inch-m4-2025-info (1)_cleaned.json",
        output_path="data/final/qa_dataset.json"
    )

if __name__ == "__main__":
    main()
