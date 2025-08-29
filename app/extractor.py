# app/extractor.py
import io
from app.utils import extract_text_from_docx, extract_text_from_pdf, identify_form_type, extract_fields
from app.excel_writer import append_to_excel

def process_uploaded_file(filename: str, content: bytes) -> dict:
    is_pdf = filename.lower().endswith(".pdf")
    buffer = io.BytesIO(content)
    
    text = extract_text_from_pdf(buffer) if is_pdf else extract_text_from_docx(buffer)
    form_type = identify_form_type(text)
    if form_type == "UNKNOWN":
        raise ValueError("Form type could not be detected")

    fields = extract_fields(text)
    fields["Source File"] = filename
    fields["Form"] = form_type

    append_to_excel(form_type, fields)
    return {"form_type": form_type, "fields": fields}
