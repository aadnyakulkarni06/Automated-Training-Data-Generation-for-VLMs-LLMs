# src/dashboard/app.py
import sys
import os
import time
import streamlit as st

# Add project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import pipeline
try:
    from src.export.run_full_pipeline import run
except ImportError:
    def run(uploaded_file):
        time.sleep(2)
        return {
            "Images_ZIP": "data/final/images.zip",
            "Annotations_JSON": "data/final/annotations.jsonl",
            "QA_Dataset_CSV": "data/final/qa_dataset.csv"
        }

# Page Config
st.set_page_config(
    page_title="Auto-Genius | Dataset Dashboard",
    layout="wide"
)

# Global Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');
            
body, h1, h2, h3, h4, p, span, div {
  font-family: "Lora", serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
}

.main {
    background-color: #f5f6f8;
}

h1, h2, h3, h4 {
    font-weight: 600;
}

p, span, div {
    text-align: center;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background-color: #ffffff;
    padding: 1.2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    text-align: center;
}

div[data-testid="stMetricValue"] {
    font-size: 26px;
    color: #2e7d32;
    text-align: center;
}

div[data-testid="stMetricLabel"] {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<h1 style='margin-top: 3rem; font-size: 3rem;'>Automated Dataset Generation</h1>", unsafe_allow_html=True)

# Ensure folders exist
folders = ["data/raw", "data/processed/images", "data/cleaned", "data/annotated", "data/final"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "File Upload", "About"], index=1)
st.sidebar.markdown("---")
st.sidebar.info(
    "Final Year Project\n\nAutomating structured dataset creation from unstructured PDFs."
)

# HOME
if page == "Home":
    st.header("Project Overview")

    st.info("This project demonstrates a fully automated system for converting unstructured documents into structured datasets for training language and vision-language models.")

    st.subheader("System Architecture")

    st.image("assets/system_architecture.png")

    st.info(
        "The pipeline integrates OCR engines and transformer-based NLP models "
        "to extract structured, training-ready data."
    )

# FILE UPLOAD
elif page == "File Upload":
    st.header("Data Ingestion and Processing")

    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
        with col2:
            st.write("")
            run_btn = st.button("Run Pipeline", type="primary", use_container_width=True)

    if uploaded_file and run_btn:
        with st.status("Executing Pipeline", expanded=True) as status:
            start_time = time.time()

            progress = st.progress(0, text="Pipeline Progress")
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            st.write("Running OCR and dataset generation...")
            outputs = run(uploaded_file)

            end_time = time.time()
            status.update(state="complete", expanded=False)

        st.subheader("Pipeline Analytics")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Processing Time", f"{round(end_time - start_time, 2)} seconds")
        with m2:
            st.metric("Artifacts Generated", len(outputs))
        with m3:
            first_file = list(outputs.values())[0]
            size_kb = round(os.path.getsize(first_file) / 1024, 2) if os.path.exists(first_file) else 0
            st.metric("Primary File Size", f"{size_kb} KB")

        with st.container(border=True):
            st.subheader("Generated Assets")
            cols = st.columns(len(outputs))
            for i, (key, path) in enumerate(outputs.items()):
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        cols[i].download_button(
                            label=f"Download {key.replace('_', ' ')}",
                            data=f,
                            file_name=os.path.basename(path),
                            use_container_width=True
                        )

    elif run_btn:
        st.warning("Please upload a PDF file before running the pipeline.")

# ABOUT
elif page == "About":
    st.header("About This Project")

    st.markdown(
        "<p style='max-width:800px;margin:auto;'>"
        "This project demonstrates a fully automated system for converting unstructured "
        "documents into structured datasets for training language and vision-language models."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.caption("Final Year Project | Cummins College of Engineering")
