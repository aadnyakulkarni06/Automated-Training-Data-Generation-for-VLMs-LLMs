from src.annotation.qa_pipeline import QAPipeline

def main():
    pipeline = QAPipeline()
    pipeline.process(
        input_path="data/cleaned/cleaned.json",
        output_path="data/final/qa_dataset.json"
    )

if __name__ == "__main__":
    main()
