import io
from app.utils import extract_text_from_docx, extract_text_from_pdf, identify_form_type, extract_fields
from app.excel_writer import append_to_excel

def process_uploaded_file(filename: str, content: bytes) -> dict:
    is_pdf = filename.lower().endswith(".pdf")
    buffer = io.BytesIO(content)

    # Extract text
    text = extract_text_from_pdf(buffer) if is_pdf else extract_text_from_docx(buffer)
    form_type = identify_form_type(text)

    if form_type == "UNKNOWN":
        raise ValueError("Form type could not be detected")

    # Extract known fields from text
    fields = extract_fields(text)
    fields["Form"] = form_type
    fields["Source File"] = filename

    # Write to Excel
    append_to_excel(fields)

    return {"form_type": form_type, "fields": fields}
