# extractor.py
from pypdf import PdfReader
from gpt_extractor import extract_field_information
import json

from docx import Document


def extract_text_from_pdf(text):
    if( text is None):
        return {"error": "No text provided for extraction"}
    
    open_ai_Data = extract_field_information(text)
    if isinstance(open_ai_Data, dict):
        return open_ai_Data
    return json.loads(open_ai_Data)

    
def extract_text_from_word(path):
    print("Extracting text from Word document:", path)
    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    page_text = {
        1: {
            "page_number": 1,
            "text": text
        }
    }
    return page_text



