import re
import pdfplumber
from docx import Document

# Matches fields like: "FIELD NAME\n(" or "FIELD NAME\n(" separated from its value
FIELD_RE = re.compile(r"([A-Z][A-Z\s/().:&-]+)\s*\(\s*([^\n]*)", re.MULTILINE)

# Known form identifiers
FORM_MAP = {
    "L20": "L20_Industry_Sale_Lease",
    "L21": "L21_Warehouse_Sale_Lease",
    "L22": "L22_Client_Requirement",
    "L24": "L24_Sale_of_Business",
}

# You can expand this based on all fields in the forms
MASTER_FIELD_LIST = [
    "NAME OF THE PERSON",
    "DESIGNATION",
    "COMPANY NAME",
    "MOBILE / TELEPHONE NUMBER",
    "E-MAIL ID",
    "STATE",
    "DISTRICT",
    "LOCATION (CITY / TOWN / VILLAGE )",
    "PLOT NO / SURVEY NO",
    "ADDRESS",
    "AVAILABLE FOR",
    "PRODUCT (s) MANUFACTURED",
    "CATEGORY",
    "PROPERTY TYPE",
    "PLOT AREA",
    "BUILT UP AREA",
    "ROOF HEIGHT (Minimum)",
    "TOTAL PRICE EXPECTED",
    "MONTHLY RENTAL BUDGET",
    "PERIOD OF LEASE",
    "ADDITIONAL INFORMATION",
    "DO YOU HAVE BCC / OC",
    "POWER",
    "WATER",
    "CRANES",
    "IS FACTORY RUNNING",
    "DO YOU HAVE NA ORDER?",
    "GRANTER OF LEASE",
    "LEASE PERIOD",
    "LEASE STARTING ON",
    "DO YOU HAVE BCC?",
    "SANCTIONED POWER",
    "SANCTIONED WATER",
    "CAPACITY OF CRANES",
    "TOTAL BUILT UP AREA",
    "TYPE OF CONSTITUTION",
    "SHARE CAPITAL",
    "NAMES OF DIRECTORS",
    "DETAILS OF THE BANKER",
    "DETAILS OF OTHER LIABILITIES IF ANY",
    "REASON FOR SALE",
    "PRODUCT RANGE",
    "YEAR OF CONSTRUCTION",
    "EXPECTED PRICE OF BUILDING (Rs.)",
    "EXPECTED RENT PER SQ.FT BUILT UP AREA (Rs.)"
    # Add more as you iterate
]

def extract_text_from_pdf(file_like) -> str:
    with pdfplumber.open(file_like) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_docx(file_like) -> str:
    doc = Document(file_like)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def identify_form_type(text: str) -> str:
    for key in FORM_MAP:
        if f"Form – {key}" in text or f"Form - {key}" in text:
            return key
    return "UNKNOWN"

def extract_fields(text: str) -> dict:
    extracted_data = {field: None for field in MASTER_FIELD_LIST}

    # Clean: remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    for field in MASTER_FIELD_LIST:
        pattern = re.escape(field) + r"\s*\(\s*([^\n]*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_data[field] = match.group(1).strip()

    return extracted_data
