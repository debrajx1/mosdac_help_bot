import os
import fitz  # PyMuPDF
from docx import Document
import pandas as pd

DOCUMENT_FOLDER = "mosdac_docs"
PARSED_OUTPUT = "parsed_docs.json"

parsed_data = {}

# Parse PDF
def parse_pdf(file_path):
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

# Parse DOCX
def parse_docx(file_path):
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

# Parse XLSX
def parse_xlsx(file_path):
    df = pd.read_excel(file_path)
    return df.to_string()

# Loop through all files
for filename in os.listdir(DOCUMENT_FOLDER):
    file_path = os.path.join(DOCUMENT_FOLDER, filename)
    try:
        if filename.endswith(".pdf"):
            parsed_data[filename] = parse_pdf(file_path)
        elif filename.endswith(".docx"):
            parsed_data[filename] = parse_docx(file_path)
        elif filename.endswith(".xlsx"):
            parsed_data[filename] = parse_xlsx(file_path)
        print(f"Parsed: {filename}")
    except Exception as e:
        print(f"Error parsing {filename}: {e}")

# Save as JSON
import json
with open(PARSED_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, indent=2, ensure_ascii=False)

print(f"Saved parsed content to {PARSED_OUTPUT}")
