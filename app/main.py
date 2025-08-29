# app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.extractor import process_uploaded_file

app = FastAPI()

# Enable frontend access later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-form")
async def upload_form(file: UploadFile = File(...)):
    if file.filename.endswith((".docx", ".pdf")):
        content = await file.read()
        try:
            extracted = process_uploaded_file(file.filename, content)
            return {"status": "success", "form_type": extracted["form_type"], "fields": extracted["fields"]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Only .docx or .pdf files are supported.")
