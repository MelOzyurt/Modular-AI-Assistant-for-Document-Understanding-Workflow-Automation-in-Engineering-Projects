# app.py
import streamlit as st
from utils.doc_parser import parse_document
from utils.summarizer import generate_summary
import json
import pandas as pd

st.set_page_config(page_title="GW Power AI Assistant", layout="wide")
st.title("⚡AI Document Assistant for Energy Projects ")


# Upload Document
uploaded_file = st.file_uploader("Upload Tender / Specification Document (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Parsing document..."):
        raw_text = parse_document(uploaded_file)
        st.success("Document successfully parsed!")

    st.subheader("📄 Extracted Text Preview")
    st.text_area("Raw Text", raw_text[:2000], height=300)

    if st.button("Generate Summary with AI"):
        with st.spinner("Generating summary with GPT..."):
            summary = generate_summary(raw_text)
            st.subheader("📋 Summary")
            st.write(summary)

            st.subheader("📤 Export")
            export_format = st.radio("Choose Export Format", ["JSON", "Excel"])
            if export_format == "JSON":
                st.download_button("Download JSON", data=json.dumps(summary, indent=2), file_name="summary.json")
            else:
                df = pd.DataFrame([summary])
                df.to_excel("summary.xlsx", index=False)
                with open("summary.xlsx", "rb") as f:
                    st.download_button("Download Excel", f, file_name="summary.xlsx")

from utils.google_sheets_handler import append_to_sheet

# Example usage after summary is generated:
sheet_id = "your_google_sheet_id"  # Found in the URL of your Google Sheet
worksheet = "Sheet1"

if st.button("Send to Google Sheets"):
    try:
        append_to_sheet(sheet_id, worksheet, summary)
        st.success("✅ Data sent to Google Sheet!")
    except Exception as e:
        st.error(f"❌ Failed to send data: {e}")

