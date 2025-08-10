# extractor.py
from pypdf import PdfReader
from gpt_extractor import extract_field_information
import json
import re



def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    pages_text = {}
    for page_num, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        cleaned = re.sub(r"\s+", " ", raw).strip()
        pages_text[page_num] = cleaned

    print("************ ++++++++ =======Extracted data : ", pages_text.items())
    open_ai_Data = extract_field_information(pages_text)

    # If the response is a dict, return it directly
    if isinstance(open_ai_Data, dict):
        return open_ai_Data
    # If it's a string, try to parse as JSON
    try:
        return json.loads(open_ai_Data)
    except Exception:
        return {"error": "Text not extract able", "raw": open_ai_Data}


def extract_text_from_document(text):
    if( text is None):
        return {"error": "No text provided for extraction"}
    
    open_ai_Data = extract_field_information(text)
    print(open_ai_Data)
    try:
        return json.loads(open_ai_Data)
    except Exception:
        return {"error": "Text not extract able", "raw": open_ai_Data}

    


