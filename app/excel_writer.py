import os
import pandas as pd
from pathlib import Path

OUTPUT_FILE = Path("client_forms.xlsx")
SHEET_NAME = "All_Form_Entries"

ALL_FIELDS = [
    "Form", "Source File", "Property For", "Property Type", "Name of Contact Person",
    "Company's Name", "Designation", "Tel. No", "Mobile No.", "Fax No.", "Email Id",
    "Address", "Country", "State", "District", "City", "Location", "Road Name/No",
    "Plot No", "Industrial Estate Name", "Building Name", "LandMark", "Total Plot Area",
    "Zone", "Total Built Up Area", "Open Area", "Operation Area", "Other Admin Area",
    "Floor Height From Ground Level (Ft.)", "Floor Level (For Gala)", "Year of Construction",
    "Do you have Building Completion Certificate", "Do you have Occupancy Certificate",
    "Is Society Formed", "Is Society Registered", "Is Property Free Hold/ Lease Hold",
    "If Lease Hold, Period Of Lease", "Starting Year Of Lease", "Granter Of Lease",
    "If Free Hold, Do you have Extract of Land Record/ (7-12)",
    "Name Of Owner As Per Land Record", "Any Objection/ Notification in Land Record",
    "Is Property Mortgaged", "Name Of Financial Institution",
    "RCC Area (Sq.Ft)", "RCC Roof Ht (Ft)", "Industrial Shed Area (Sq.Ft)",
    "Industrial Shed Roof Ht (Ft)", "Total Area", "Power Sanctioned (in HP)",
    "Power Connection Status", "Connected/Disconnected Power (in HP)",
    "Water Connection Status", "Water", "Crane", "Crane Capacity",
    "NOC from Department Of Industry", "Consent Of Pollution Control Dept",
    "Membership Of CEPT", "Product/s being Manufactured", "Is Factory Running",
    "If No, Closed Since", "Can Premise be used as Warehouse",
    "The Premise Is Ideally Suited For", "Financial Institution A.",
    "Financial Institution B.", "Financial Institution C.", "Labor Dues",
    "Electricity Dues", "Water Dues", "Property Tax",
    "Sales Tax/ Income Tax/ Excise & Custom Dues", "Other Liabilities",
    "Total Liabilities", "Comments Of Seller",
    "Will You Provide Required NOCs for Sale/ Transfer of Lease Hold Rights",
    "Expected Price Plot (Rs.)", "Expected Price Of Building (Rs.)",
    "Expected Price of Plant + Machinery (Rs.)", "Expected Price of Other Amenities (Rs.)",
    "Total Expected Price (Rs.)", "Option to Sell Only Plot + Building",
    "Other Terms (If Any)", "Period (No. Of Years)",
    "Expected Rent Per Sq.Ft Built Up Area (Rs.)", "Expected Rent Per Sq.Ft. Open Area (Rs.)",
    "Expected Rent For Machinery (Rs.)", "Total Expected Rent Per Month (Rs.)",
    "Deposit Expected (Rs.)", "Additional Information (If Any)",
    "Registration No", "Name of Agent", "Date of Registration",
    "Name of Facilitator", "Requirement Confirmed By Manager",
    "Requirement Confirmed By Director"
]

def append_to_excel(data: dict):
    df_new = pd.DataFrame([data])
    df_new = df_new.reindex(columns=ALL_FIELDS)  # Ensure consistent column order

    if OUTPUT_FILE.exists():
        with pd.ExcelWriter(OUTPUT_FILE, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            try:
                existing = pd.read_excel(writer.path, sheet_name=SHEET_NAME)
                df_combined = pd.concat([existing, df_new], ignore_index=True)
                df_combined.to_excel(writer, sheet_name=SHEET_NAME, index=False)
            except ValueError:
                df_new.to_excel(writer, sheet_name=SHEET_NAME, index=False)
    else:
        with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
            df_new.to_excel(writer, sheet_name=SHEET_NAME, index=False)
