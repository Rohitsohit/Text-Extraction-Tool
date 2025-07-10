# extractor.py

import fitz
from docx import Document
from gpt_extractor import extract_field_information
from field_descriptions import field_descriptions_details
import json


#  PDF extractor with page + context
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)

    # Step 1: Collect all page texts
    pages_text = []
    results = []
    for page_num, page in enumerate(doc, start=1):
        cleaned = ' '.join(page.get_text().split())
        pages_text.append((page_num, cleaned))
        try:
                open_ai_Data = extract_field_information(pages_text)
                if open_ai_Data and open_ai_Data != "{}":
                    parsed = json.loads(open_ai_Data)
                    results.append(parsed)
                    break
        except:
                continue
    return results
