# app/excel_writer.py
import os
import pandas as pd
from app.utils import FORM_MAP
from pathlib import Path

OUTPUT_FILE = Path("client_forms.xlsx")

def append_to_excel(form_key: str, data: dict):
    sheet = FORM_MAP[form_key]
    df_new = pd.DataFrame([data])

    if OUTPUT_FILE.exists():
        with pd.ExcelWriter(OUTPUT_FILE, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            try:
                existing = pd.read_excel(writer.path, sheet_name=sheet)
                df_combined = pd.concat([existing, df_new], ignore_index=True)
                df_combined.to_excel(writer, sheet_name=sheet, index=False)
            except ValueError:
                df_new.to_excel(writer, sheet_name=sheet, index=False)
    else:
        with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
            df_new.to_excel(writer, sheet_name=sheet, index=False)
