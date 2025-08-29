# app/utils.py
import re
import pdfplumber
from docx import Document

FORM_MAP = {
    "L20": "L20_Industry_Sale_Lease",
    "L21": "L21_Warehouse_Sale_Lease",
    "L22": "L22_Client_Requirement",
    "L24": "L24_Sale_of_Business",
}

def identify_form_type(text: str) -> str:
    for key in FORM_MAP:
        if f"Form – {key}" in text or f"Form - {key}" in text:
            return key
    return "UNKNOWN"

def extract_text_from_pdf(file_like) -> str:
    with pdfplumber.open(file_like) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_docx(file_like) -> str:
    doc = Document(file_like)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_fields(text: str) -> dict:
    fields = {
        "Name": re.search(r"NAME OF THE PERSON\s*\((.*?)\)", text, re.DOTALL),
        "Company": re.search(r"COMPANY NAME\s*\((.*?)\)", text, re.DOTALL),
        "Mobile": re.search(r"TELEPHONE NUMBER\s*\((.*?)\)", text, re.DOTALL),
        "Email": re.search(r"E-?MAIL ID\s*\((.*?)\)", text, re.DOTALL),
    }
    return {k: (v.group(1).strip() if v else "") for k, v in fields.items()}
