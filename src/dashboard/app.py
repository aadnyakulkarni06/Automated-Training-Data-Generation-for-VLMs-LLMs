# src/dashboard/app.py
from pathlib import Path
import sys
import streamlit as st
import os

# Fix Python module imports
CURRENT_FILE = Path(__file__).resolve()
SRC_DIR = CURRENT_FILE.parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ingestion.ingestion_pipeline import process_pdf

# Streamlit Setup
st.set_page_config(page_title="Automated Dataset Dashboard", layout="wide")
st.title("Automated Dataset Generation for LLM & VLM Training")

# Ensure folders exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed/images", exist_ok=True)
os.makedirs("data/cleaned", exist_ok=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "File Upload", "About"])

# Pages
if page == "Home":
    st.header("🏠 Home")
    st.write("Welcome to the **Automated Dataset Generation Dashboard**.")

elif page == "File Upload":
    st.header("📂 Upload a PDF File")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file:
        st.success(f"📁 File selected → {uploaded_file.name}")

        if st.button("Start Processing 🚀"):
            with st.spinner("Running ingestion pipeline..."):
                cleaned_output_path = process_pdf(uploaded_file)

            st.success("🎯 Processing Completed Successfully!")

            st.info(
                "🗂 Output Locations:\n"
                "- Raw PDF → `data/raw/`\n"
                "- Extracted Images → `data/processed/images/`\n"
                "- OCR JSON → `data/processed/`\n"
                "- Cleaned JSON → `data/cleaned/`\n"
            )

            st.write(f"✨ Cleaned output generated at: **{cleaned_output_path}**")

            # Optional download button
            with open(cleaned_output_path, "rb") as cleaned_file:
                st.download_button(
                    label="⬇️ Download Cleaned JSON",
                    data=cleaned_file,
                    file_name=os.path.basename(cleaned_output_path),
                    mime="application/json"
                )

elif page == "About":
    st.header("ℹ️ About This Project")
    st.write(
        "This dashboard automates dataset generation from document sources using "
        "PDF-to-image conversion, OCR, and text cleaning."
    )