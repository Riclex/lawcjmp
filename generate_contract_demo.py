#!/usr/bin/env python3
from docxtpl import DocxTemplate
import pandas as pd
import os
import subprocess


TEMPLATE = "contract_template.docx"
DATA_FILE = "sample_contract_data.csv"
OUTPUT_DIR = "output_contracts"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Load data
df = pd.read_csv(DATA_FILE)
record = df.iloc[0].to_dict()

# Render contract
tpl = DocxTemplate(TEMPLATE)
tpl.render(record)
docx_path = os.path.join(OUTPUT_DIR, f"CONTRACT_{record['employee_name']}.docx")
tpl.save(docx_path)
print(f"[ok] DOCX generated: {docx_path}")

print(f"[ok] Contract generated: {output_path}")

# PDF conversion (cross-platform via LibreOffice headless mode)
try:
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf",
        "--outdir", OUTPUT_DIR, docx_path
    ], check=True)
    print(f"[ok] PDF generated in {OUTPUT_DIR}")
except Exception as e:
    print("[warn] PDF conversion failed. Install LibreOffice and ensure it's in PATH.")
