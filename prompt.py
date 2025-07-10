field_descriptions_details = {
    "Document Name": "Construct the name using: '(artist_name) - (project_name or song_name) (execution_status)'. If no project, use song name. If multiple songs, list them comma-separated. Output exact name only.",
    "Execution Status": "Check signature sections. If all parties signed -> FX (Fully-Executed) . If only client signed -> PX (Payer to Sign). If only counterparty signed -> PX (Payee to Sign). If none signed -> NX (No Execution). Use keywords like 'Signed', 'Executed'.",
    "Song Title": "Look in first 1-3 paragraphs or in Schedule 1’s or LOD’s. Search for keywords like 'Composition entitled', 'Master recording entitled', 'Song titled'. Return exact name(s) only.",
    "Artist Name": "Usually in first paragraph. Look for 'Artist' designation or references to 'performances of Artist', 'recording artist', etc.",
    "Single/Multisong Line": "Appears in first 2 paragraphs. Single: 'one (1) master recording'. Multi: references to 'album', 'mixtape', or multiple masters.",
    "Client Party": "Referred to as 'you', 'your', or 'Producer'. Found in first paragraph. May be named explicitly.",
    "Direct Counterparty": "Usually denoted as 'we', 'us', or 'our'. Could be the label or artist\u2019s company.",
    "Alternative Counterparties": "Mentioned as 'Label', 'Distributor', or company names like 'Warner'. Indicates third parties with obligations but not main signatories.",
    "Classification of Recoupment Language": "Find paragraph with 'recoup'. Look for logic like: 'no royalty until recording costs recouped', 'retroactive royalty after recoupment', or 'from net artist royalties'.",
    "Effective Date": "Usually in the first paragraph. Look for 'Effective as of...', or 'Agreement dated as of...'.",
    "Distributor": "Look for 'Released by [Distributor]' or 'Distributed by'. May be same as Label.",
    "Label": "Look for 'Owned by', 'a division of', or 'Released by [Label]'. Match known label names if needed.",
    "Lawyer Information": "Search for lines starting with 'C/O'. Two lawyers: one for Client Party, one for Counterparty.",
    "Producer Royalty Points": "Look for sections with 'Royalty', 'points', 'Base Rate', 'NAR', or 'PPD'. Extract the numeric value.",
    "Type of Royalty (NAR or PPD)": "NAR \u2192 'net artist royalties', 'from artist\u2019s share'. PPD \u2192 'wholesale price', 'price to dealers'. Check if royalty is based on NAR or PPD.",
    "Bumps": "Rare. Look for clauses saying royalties increase after certain units sold. Example: 'royalty increases after 50,000 units'.",
    "Third Party Money": "Found in SoundExchange LOD at the end. Extract any additional payees other than client/counterparty.",
    "Producer Advance": "Look for 'Advance' section. Return dollar amount, e.g. '$15,000'. May be in Schedule A.",
    "Producer Advance Recoupment Classification": "Appears before/after Advance. Mentions recoupment policy, e.g., 'Advance shall be recoupable...'.",
    "Producer Advance Legal Recoupment": "Sentences describing legal treatment of Advance, e.g., 'Advance deemed fully recoupable'.",
    "Organization Counting Sales Units": "Look for 'USNRC Net Sales', 'Net Sales Units', or similar phrases. May include definition.",
    "International Sales Policy": "Find paragraph mentioning 'outside the United States', 'international sales', or 'global commercial exploitation'."
}


def build_final_document_prompt(full_document_text: str) -> str:
    field_list_text = "\n".join(
        [f"{i+1}. **{name}**\n   {desc}" for i, (name, desc) in enumerate(field_descriptions_details.items())]
    )

    return f"""
You are an intelligent document analysis agent tasked with extracting specific field values from a music royalty contract.

Below are 22 fields you must extract. Each field includes a detailed description of what it means and how to identify it.

Your task is:
- Read all pages of the contract (provided below).
- For each field:
    - Use the field description as instruction to identify the correct value.
    - If you are confident the value is found, return it.
    - If not found in the entire document, return "not found".

Return the results as a single JSON object (one key per field) only after the last page is processed.

---

### Fields to Extract:
{field_list_text}

---

### Contract Text:
\"\"\"
{full_document_text}
\"\"\"

---

### Output Format (after the last page):
{{
  "Document Name": "...",
  "Execution Status": "...",
  "Song Title": "...",
  ...
  "International Sales Policy": "not found"
}}
"""