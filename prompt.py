def build_field_prompt(field_name: str, field_description: str, page_number: int, page_text: str) -> str:
    return f"""
You are an expert in reading and understanding music royalty contracts. Please extract the field: **{field_name}**.

Field Description:
{field_description}

Page Text:
\"\"\"
{page_text}
\"\"\"

Return your answer in this format:
{{
  "field_name": "{field_name}",
  "value": "...",
  "page_number": {page_number},
  "confidence": "High/Medium/Low",
  "context": "...short reason why you chose this..."
}}

If not found on this page, return:
{{
  "field_name": "{field_name}",
  "value": null,
  "page_number": {page_number},
  "confidence": "None",
  "context": "Field not found on this page."
}}
"""