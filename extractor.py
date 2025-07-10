# extractor.py

import fitz
from docx import Document
from gpt_extractor import extract_field_information
from field_descriptions import field_descriptions_details
import json


#  Shared keywords
KEYWORDS = ["song title"]

#  PDF extractor with page + context
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    results = []
    found_fields = set()
    for field,desc in field_descriptions_details.items():
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            cleaned_page_text = ' '.join(text.split())
            open_ai_Data=extract_field_information(field, desc, page_num, cleaned_page_text)
            if open_ai_Data and open_ai_Data !="{}":
                try:
                    parsed =json.loads(open_ai_Data)
                    parsed["page_number"] = page_num
                    parsed["field"] =field
                    results.append(parsed)
                    # found_fields.add(field)
                    break
                except:
                    continue
        if(len(found_fields) == len(field_descriptions_details)):
            break                    
    return results

# Word extractor with paragraph index + context
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    results = []

    for idx, para in enumerate(paragraphs):
        for keyword in KEYWORDS:
            if keyword.lower() in para.lower():
                context = paragraphs[max(0, idx-2): idx+3]
                results.append({
                    "paragraph_index": idx + 1,
                    "keyword": keyword,
                    "match": para,
                    "context": context
                })

    return results