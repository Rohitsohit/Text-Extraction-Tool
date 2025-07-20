# extractor.py
import fitz
from gpt_extractor import extract_field_information
import json
import re

#  PDF extractor with page + context
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)

    # Step 1: Collect all page texts
    results = []
    pages_text = {}  # initialize as a dictionary
    for page_num, page in enumerate(doc, start=1):
        cleaned = ' '.join(page.get_text().split())
        pages_text[page_num] = cleaned 

    print("************ ++++++++ =======Extracted data : ",pages_text.items())   
    open_ai_Data = extract_field_information(pages_text)

    if open_ai_Data and open_ai_Data.strip() not in ["", "{}", "None"]:
        try:
            open_ai_Data = re.sub(r"^```json\s*|\s*```$", "", open_ai_Data.strip(), flags=re.IGNORECASE)
            parsed = json.loads(open_ai_Data)
            results.append(parsed)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to decode JSON: {e}")
            print(f"[DEBUG] Raw OpenAI response: {repr(open_ai_Data)}")
    return results
