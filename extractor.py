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


def extract_text_from_document(path: str):

    print(f"[DEBUG] Starting PDF parse: {path}")
    try:
        reader = PdfReader(path)

        if getattr(reader, "is_encrypted", False):
            print("[WARN] PDF is encrypted. Attempting empty-password decrypt…")
            try:
                reader.decrypt("")
            except Exception as e:
                print(f"[ERROR] Decrypt failed: {e}")
                return "Text not extract able"

        num_pages = len(reader.pages)
        print(f"[DEBUG] PDF opened. Total pages: {num_pages}")

        pages_text = {}
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                print(f"[DEBUG] Extracting text from page {page_num}")
                raw = page.extract_text() or ""
                cleaned = re.sub(r"\s+", " ", raw).strip()
                pages_text[page_num] = cleaned
            except Exception as e:
                print(f"[WARN] Failed to extract page {page_num}: {e}")
                pages_text[page_num] = ""

        print(f"[DEBUG] Extraction done. Page count: {len(pages_text)}")

        # Check if we have meaningful text in at least one page
        combined_text = " ".join(pages_text.values()).strip()
        meaningful_chars = sum(ch.isalnum() for ch in combined_text)
        if not combined_text or meaningful_chars < 10:
            return "Text not extract able"

        # Debug print of extracted data
        print("************ ++++++++ =======Extracted data :", pages_text.items())

        # Step 2: Pass extracted text dictionary to your AI function
        try:
            print("[DEBUG] Passing pages_text to extract_field_information()")
            response = extract_field_information(pages_text)
            if isinstance(response, dict):
                return response
            else:
                # If not dict, try to parse as JSON
                try:
                    return json.loads(response)
                except Exception:
                    return {"error": "Text not extract able", "raw": response}
        except Exception as e:
            print(f"[ERROR] Failed in extract_field_information: {e}")
            return {"error": "Text not extract able"}

    except Exception as e:
        print(f"[ERROR] Failed to parse PDF: {e}")
        return {"error": "Text not extract able"}


