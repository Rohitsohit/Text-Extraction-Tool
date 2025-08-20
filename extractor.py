# extractor.py
from pypdf import PdfReader
from gpt_extractor import extract_field_information
import json


def extract_text_from_pdf(text):
    if( text is None):
        return {"error": "No text provided for extraction"}
    print("[DEBUG] Extraction started for text")
    open_ai_Data = extract_field_information(text)
    if isinstance(open_ai_Data, dict):
        return open_ai_Data
    return json.loads(open_ai_Data)

    
def extract_text_from_word(path):
    print("Extracting text from Word document:", path)
    
    return path



