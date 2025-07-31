# utils/doc_parser.py

from io import BytesIO
from docx import Document
import PyPDF2

def parse_document(uploaded_file) -> str:
    """
    Extract text from uploaded PDF or DOCX file.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        Extracted raw text as a string.
    """
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        return extract_text_from_docx(uploaded_file)
    else:
        return "Unsupported file type."

def extract_text_from_pdf(file) -> str:
    pdf_reader = PyPDF2.PdfReader(file)
    text = []
    for page in pdf_reader.pages:
        text.append(page.extract_text())
    return "\n".join(text)

def extract_text_from_docx(file) -> str:
    # We use BytesIO since uploaded_file is a byte stream
    doc = Document(BytesIO(file.read()))
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)
