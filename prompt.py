from descriptons import document_name_description,legal_advance_recoupment_description,recoupment_classification_description,producer_royalty_points_description,type_of_royalty_description,lawyer_information_description,label_description,distributor_description,effective_date_description,alternative_counterparties_description,direct_counterparty_description,client_party_description,single_or_multisong_line_description,execution_status_description,artist_name_description,song_title_description,recoupment_language_description,international_sales_policy_description,organization_counting_sales_units_description,producer_advance_legal_recoupment_description,third_party_money_description,bumps_description


field_descriptions_details = {

    "Label owner": label_description,
    "Recoupment Classification": recoupment_classification_description,
    "Organization Counting Sales Units": organization_counting_sales_units_description,
}


def build_final_document_prompt(pages_text: dict) -> str:
    field_list_text = "\n".join(
        [f"{i+1}. **{name}**\n   {desc}" for i, (name, desc) in enumerate(field_descriptions_details.items())]
    )

    # Prepare contract text by adding page number headers
    contract_text = "\n".join(
        [f"\n--- Page {page_num} ---\n{text}" for page_num, text in pages_text.items()]
    )

    return f"""
You are an intelligent document analysis agent tasked with extracting specific field values from a music royalty contract.

Below are the fields you must extract. Each field includes a detailed description of what it means and how to identify it.

Your task is:
- Read all pages of the contract (provided below).
- For each field:
    - Use the field description as instruction to identify the correct value.
    - If you are confident the value is found, return:
        {{
          "value": "actual value here",
          "page_number": X
        }}
    - If not found in the entire document, return:
        {{
          "value": "not found",
          "page_number": null
        }}

Return the results as a single JSON object (one key per field) only after the last page is processed.

---

### Fields to Extract:
{field_list_text}

---

### Contract Text:
\"\"\"
{contract_text}
\"\"\"

---

### Output Format (after the last page):
{{
  "Document Name": {{
    "value": "...",
    "page_number": 2
  }},
  "Execution Status": {{
    "value": "...",
    "page_number": 4
  }},
  ...
  "International Sales Policy": {{
    "value": "not found",
    "page_number": null
  }}
}}
"""