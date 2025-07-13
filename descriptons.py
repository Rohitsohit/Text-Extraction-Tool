document_name_description = """
Extract the **Document Name** using the format described below. This value is typically constructed based on key metadata like artist name, project name, song title(s), and execution status.

Expected formats:
1. If project name is present:
   "(artist_name) - (project_name) (execution_status)"
2. If no project name is found:
   "(artist_name) - (song_name) (execution_status)"
3. If multiple song names are found:
   "(artist_name) - (song_name_1), (song_name_2) (execution_status)"

Instructions:
- Look for mentions of the **artist name**, **project name**, **song title(s)**, and **execution status** within the document.
- Execution status can be one of: FX (Fully-Executed), PX (Partially-Executed), NX (No Execution).
- Use only the values that are present — if the project name is not available, fall back to song name(s).

Output should be a single constructed string in one of the valid formats listed above.
"""

execution_status_description = """
Determine the **Execution Status** of the agreement by analyzing the signature section.

Your task is to identify whether the document has been fully, partially, or not executed by the relevant parties.

Rules:
1. If **all signature blanks are signed**, return → "FX" (Fully-Executed)
2. If **some signatures are missing**:
   - If **client party signed** but **counterparty did not**, return → "PX" (Partially-Executed - Payer to Sign)
   - If **counterparty signed** but **client party did not**, return → "PX" (Partially-Executed - Payee to Sign)
3. If **no signatures** are found, return → "NX" (No Execution)

Look for variations of the word "Signed" or "Executed" and identify which parties are associated with completed or blank signature fields.

Return only one of the following values:
- "FX"
- "PX"
- "NX"
"""

song_title_description = """
Extract the **Song Title** or **titles** from the agreement. These will typically appear in one of the following forms:

1. In the first 1–3 paragraphs, often introduced with terms like:
   - “master recording entitled...”
   - “musical composition entitled...”
   - “(the ‘Composition’)” or “(the ‘Master’)”

2. Later in the document — often in tables under:
   - “Schedule 1”
   - “List of Master(s)” or “List of Composition(s)”
   - “LOD” (Letter of Direction)

Common indicators:
- The song title will appear in **quotation marks** and is often preceded by phrases like:
  - “entitled ‘[Title]’”
  - “titled ‘[Title]’”
  - “composition entitled ‘[Title]’”
  - “master recording entitled ‘[Title]’”

Examples:
- “Code + Love me sum more”
- “Cap”
- “Herb”
- “You’re Lost”
- “Jungle”
- “Midnight”

Your task is to return only the **actual title(s)** (e.g., `"Herb"`, `"Cap"`), not the surrounding explanation.

If multiple song titles are present, return them as a **comma-separated string**.

"""

artist_name_description = """
Extract the **Artist Name** from the document. It will always appear in the **first paragraph** and be immediately followed by the label **("Artist")**.

What to look for:
- A proper name or entity followed by:
  - (“Artist”)
  - ("the Artist")
  - (‘Artist’)

Examples:
- “Drake (“Artist”)”
- “Beyoncé (the ‘Artist’)”
- “Travis Scott (‘Artist’)”

Expected Output:
- Return only the **artist name** without quotes or labels.
"""

single_or_multisong_line_description = """
Extract the **Single/Multisong Line** from the agreement. This information should be located within the **first two paragraphs** of the document.

What to look for:
- Language indicating the agreement is *“in connection with”* a master recording or multiple masters.
- References to:
  - “one (1) master”
  - “multiple master recordings”
  - “recordings entitled...”
- Mentions of projects may include terms such as:
  - (“Album”)
  - (“Project”)
  - (“Mixtape”)

This field helps identify whether the agreement is for a **single song**, **multiple songs**, or a broader project.

Expected Output:
- A phrase indicating the scope of the agreement, such as:
  - “one (1) master recording”
  - “multiple master recordings”
  - “an album entitled ‘XYZ’”
"""


client_party_description = """
Extract the **Client Party** from the agreement. This is the individual or entity being addressed in the contract, and will almost always appear in the **opening paragraph**.

What to look for:
- The client is typically referred to as:
  - “you”
  - “your”
  - “Producer” or “the Producer”

- Look for a proper name or company referenced at the beginning, followed by phrases like:
  - “(referred to herein as ‘you’)”
  - “(‘Producer’)”

Your task is to extract the **name of the client party** — typically a person or entity to whom the agreement is directed.

Expected Output:
- Only the **name** of the individual or company being addressed (e.g., “Jane Doe” or “XYZ Productions”).

"""

direct_counterparty_description = """
Extract the **Direct Counterparty** from the agreement. This is the party issuing the agreement and is typically referred to using the terms:
- “we”
- “us”
- “our”
- Sometimes also labeled as “Artist”

What to look for:
- These terms will often appear in the first 1–2 paragraphs.
- The counterparty may be a company, label, or artist name and often appears alongside:
  - A definition such as: “(hereinafter referred to as ‘we’ or ‘Company’)”
  - A context line such as: “we are engaging you...”

You can also look at:
- **Schedule A**
- **SoundExchange LOD** section at the end of the document

Use cross-reference cues from the same page or section where **Song Title** and **Artist Name** are identified.

Expected Output:
- The **name of the label, artist, or entity** acting as the issuer of the agreement (e.g., “Atlantic Records” or “Drake”).

"""

alternative_counterparties_description = """
Extract the names of any **Alternative Counterparties** — parties that may be contractually liable or involved, even if they are not the primary counterparty.

What to look for:
- Entities that may be referenced as:
  - “Label”
  - “Distributor”
  - “Licensee”
  - “Third-party payor”
- These names may **not be explicitly defined**, but often appear alongside royalty, rights, or distribution language.
- Often listed in sections dealing with:
  - Rights assignment
  - Revenue flow
  - SoundExchange, Schedule A, or signature blocks

Heuristics:
- Common major and independent **labels** and **distributors** frequently appear across contracts (e.g., “Empire”, “Ingrooves”, “The Orchard”, “Sony Music”, “Universal”, etc.).
- These can appear in clauses like:
  - “...via our distributor, Empire Distribution...”
  - “...subject to the rights of XYZ Records...”
  - “...as agreed by Label or any affiliated third-party rights holder...”

Expected Output:
- A **list of entity names** representing alternative counterparties, if present.

"""


recoupment_language_description = """
Extract the section(s) from the document that define when and how the Producer becomes eligible for royalty payments, based on recoupment of certain costs.

You're looking for language related to the Producer's Royalty being contingent upon recoupment of Recording Costs, Advances, or Approved Budgets from Net Artist Royalties or similar pools.

Trigger Logic to Identify:
- Look for phrases like:
  - "No royalty shall be payable until..."
  - "Producer's Royalty shall be paid retroactively from record one after..."
  - "After recoupment of Recording Costs..."
  - "Unless and until Company has recouped..."

What is Being Recouped:
- Recording Costs
- Advances / Producer Advance
- Approved Budgets
- Sometimes: Sample Clearance Costs, Out-of-pocket costs

What is Excluded from Recoupment:
- In-pocket advances paid to Artist
- Third-party advances (e.g., mixers, co-producers)
- Marketing or Mechanical royalties

Source of Recoupment Pool:
- "Net Artist Royalties"
- "Net Artist Rate"
- "Net Royalty" (Artist’s all-in royalty minus participant royalties)

Recoupment Limits:
- Look for clauses like "Advance shall be recouped one time only" or "for the avoidance of doubt" to identify limitations on double deductions.

Your task is to extract the full sentence or paragraph that explains this recoupment mechanism. If multiple statements contribute to the explanation, return them together as a block of text.

If such language is not found in the document, return: { "field": "Classification of Recoupment Language", "value": "Not Found" }
"""

effective_date_description = """
Extract the **Effective Date** of the agreement. This will always be found in the **first paragraph** of the document.

What to look for:
- If there is only **one date** on the first page, that is the Effective Date.
- If there are **multiple dates** on the first page, select the one that is explicitly labeled or introduced with:
  - “Effective as of...”
  - “This agreement is effective...”
  - “Effective Date:”

Expected Output:
- A **date string** in a common format (e.g., “January 1, 2023” or “01/01/2023”)

"""

distributor_description = """
Extract the **Distributor** involved in the agreement. This may be **explicitly labeled as "Distributor"**, or it may appear contextually using phrases such as:

- “released by [Entity]”
- “distributed by [Entity]”
- “[Entity], a division of [Parent Company]”

Common placements:
- In the opening paragraph or in sections describing ownership, release rights, or label hierarchy
- May appear alongside the label or be synonymous with the **Label** itself

Heuristic:
- If the **Distributor** is not explicitly stated but the **Label** is, and there is no conflicting information, it is typically safe to assume the **Label and Distributor are the same**.

Example:
- “released by Atlantic Records, a division of Warner Music Group (“Company”)”

Expected Output:
- The **name of the distributor** (e.g., “Atlantic Records”, “Empire”, “The Orchard”)

"""

label_description = """
Extract the **Label** referenced in the agreement. This is often defined as “Label” but may also appear implicitly through associated terms or structures.

What to look for:
- Explicit phrases such as:
  - “Label”
  - “owned by [Parent Company]”
  - “released by [Label Name]”
  - “a division of [Parent Company]”
- Common clause formats:
  - “[Label Name], a division of [Company]”
  - “[Label Name] (“Label”)”
  - “Label: [Entity]”

Heuristic:
- If not explicitly labeled as “Label”, but one entity is described with ownership or distribution context (e.g., “released by Atlantic Records”), you may assume that entity is the **Label**.
- If **Distributor** is mentioned and **Label** is not, and there’s no conflict, it is often safe to assume they are the same.

Database Matching:
- Cross-reference the extracted name with a pre-loaded list of known Labels for validation (e.g., “Atlantic Records”, “Empire”, “Republic”, “The Orchard”).

Expected Output:
- The **name of the label** (e.g., “Atlantic Records”)

"""

lawyer_information_description = """
Extract the **Lawyer Information** from the agreement. These will typically be listed using the label **“C/O”** (care of), and there are usually **two parties** listed.

What to look for:
- Lines or blocks containing:
  - “C/O [Law Firm or Lawyer Name]”
  - Address blocks or contact details beginning with “C/O”
- Usually, both the **Client Party’s lawyer** and the **Counterparty’s lawyer** are listed.

Identification Strategy:
1. Pull both “C/O” entries and their associated names.
2. Whichever lawyer block is **closer to the Artist Name** should be tagged as:
   - `"client_lawyer": "<lawyer info>"`
3. The other should be:
   - `"counterparty_lawyer": "<lawyer info>"`

Expected Output:
```json
{
  "client_lawyer": "C/O XYZ Law Group, 123 Main St, New York, NY",
  "counterparty_lawyer": "C/O ABC Legal LLP, 456 Sunset Blvd, Los Angeles, CA"
}
"""

producer_royalty_points_description = """
Extract the **Producer Royalty Points** from the agreement. This refers to the numerical value(s) of royalties awarded to the producer, typically expressed as a percentage of Net Artist Royalties (NAR) or PPD (Published Price to Dealer).

Where to Look:
- Locate the **royalty clause**, usually labeled as **Clause 4 to 7** in the agreement.
- Look for sections containing phrases such as:
  - “Producer Royalty”
  - “Base Rate”
  - “Royalty Points”
  - “X% of Net Artist Royalties” or “X% of PPD”
  - “equal to ___ percentage points”

Expected Characteristics:
- The clause will often contain **one or more numerical values (e.g., 3%, 5 points)** linked to:
  - **NAR (Net Artist Royalty/Rate)**
  - **PPD (Published Price to Dealer)**
- It may describe splits, escalations, or alternative configurations (e.g., “3 points escalated to 4 after 100,000 units sold”)

Expected Output:
- Only the relevant royalty percentage or point values tied to the producer, like:
  - “3% of NAR”
  - “5 points on PPD”
  - “Base rate of 4%”
"""


type_of_royalty_description = """
You are reviewing a music contract to determine the basis on which the Producer's royalty is calculated. There are only two acceptable values for this field:

- "NAR" – Net Artist Rate / Royalties
- "PPD" – Published Price to Dealers

Do NOT return a default or inferred value. You must be extremely confident based on explicit language in the document. If confidence is not high, return "Not Found".

Understanding the Two Options:

1. NAR (Net Artist Rate)
- The royalty is calculated as a percentage of the Artist’s royalties.
- It is a piece of the artist’s pie — the producer only gets paid after the artist's share is allocated.

Keywords/Indicators:
- "net artist rate"
- "net artist royalties"
- "calculated on the same basis as Artist’s royalties"
- "from the ‘net artist royalties’"
- Definitions using: 
  - "gross all-in royalties payable to Artist minus royalties payable to Producer and other royalty participants"

2. PPD (Published Price to Dealers)
- The royalty is calculated as a percentage of the wholesale price — a fixed monetary base.
- This is often a more favorable basis for the producer.

Keywords/Indicators:
- "PPD"
- "Published Price to Dealers"
- "wholesale price"
- "price to dealers"
- "royalty based on the wholesale rate"

Extraction Instructions:

1. High-Confidence Match (Primary Signal)
   - If you find “PPD” or “Published Price to Dealers” used explicitly in the context of royalty calculation → return "PPD".
   - If you find “net artist royalties” or “net artist rate” in royalty calculation context → return "NAR".

2. Supporting Clauses (Secondary Signal)
   For NAR:
   - Phrases showing that producer royalties are deducted from the artist’s share.
   - Definitions involving "gross royalties payable to artist minus..."

   For PPD:
   - Simple language showing producer gets X% of wholesale price.
   - Absence of any mention of artist’s share or net definitions.

Return Format:
{
  "field": "Type of Royalty",
  "value": "NAR"
}
or
{
  "field": "Type of Royalty",
  "value": "PPD"
}
or
{
  "field": "Type of Royalty",
  "value": "Not Found"
}

Important: If you're not highly confident based on the explicit text, do not guess. Return "Not Found".
"""


organization_counting_sales_units_description = """
Extract the **unit of measurement** used to count sales for royalty calculations — such as "units," "albums," "downloads," or "streams."

Look for definitions or references to **USNRC Net Sales** or similar phrases that describe what counts as a sale. You do NOT need to extract the full paragraph — only the **unit** used for sales measurement.

Key phrases to look for:
- "USNRC Net Sales"
- "Net Sales (USNRC)"
- "sales through normal retail channels"
- "each album sold"
- "per download"
- "streamed units"

The correct output should be a **single word or phrase** representing the sales unit, such as:
- "units"
- "albums"
- "digital downloads"
- "streams"
- "physical records"

"""

third_party_money_description = """
Extract the **single monetary amount or percentage** that represents the share of royalties to be paid to a third party, such as a Producer, Mixer, or Co-producer.

This value will typically appear in the **SoundExchange LOD (Letter of Direction)** section, usually located **at the end of the document**.

You are NOT required to extract the full paragraph or explanation — just the **specific value** (e.g., "$10,000" or "5%").

Look for language that includes:
- "pay directly to [Name/Entity] X%"
- "SoundExchange shall remit X%"
- "monies payable to [third party] in the amount of $X"
- "payment of $X or X% to [third party]"

If multiple values are listed, prioritize the **clearest standalone percentage or amount** tied to a third-party payment directive.

"""

organization_counting_sales_units_description = """
Extract the **unit of measurement** used to count sales for royalty calculations — such as "units," "albums," "downloads," or "streams."

Look for definitions or references to **USNRC Net Sales** or similar phrases that describe what counts as a sale. You do NOT need to extract the full paragraph — only the **unit** used for sales measurement.

Key phrases to look for:
- "USNRC Net Sales"
- "Net Sales (USNRC)"
- "sales through normal retail channels"
- "each album sold"
- "per download"
- "streamed units"

The correct output should be a **single word or phrase** representing the sales unit, such as:
- "units"
- "albums"
- "digital downloads"
- "streams"
- "physical records"

"""


producer_advance_legal_recoupment_description = """
Extract the **exact monetary amount** specified as the **Producer Advance** in the contract. You do NOT need to return the full sentence — only the **dollar value** (e.g., "$10,000", "$7,500", "USD 5,000").

What to look for:
- Amounts mentioned near terms like:
  - "Producer Advance"
  - "Advance payable to Producer"
  - "Advance of $X"
- These will typically appear in legal or financial sections of the contract.
- The value may also appear alongside phrases like:
  - "shall be recoupable"
  - "recouped from royalties"
  - "recouped from Producer’s share"

Expected Output:
- Only the **money value** (e.g., "$10,000")

If no such amount is found, return:
{ "field": "Producer Advance Legal Recoupment", "value": "Not Found" }
"""




##########################################################################################
international_sales_policy_description = """
Extract the full paragraph(s) or section(s) from the document that describe the policy or conditions related to international sales of the work.

You are specifically looking for any language that addresses the commercial exploitation, distribution, or royalty treatment of the content outside the United States.

Language to look for:
- "commercial exploitation outside the United States"
- "international"
- "foreign sales" / "foreign exploitation"
- "outside the U.S." or "outside the United States"
- Mentions of royalties, deductions, or variations in payments based on international markets

The goal is to capture the entire paragraph or section that includes this type of language. If multiple relevant paragraphs exist, return all of them as a block of text.

"""

bumps_description = """
Extract any language that refers to **percentage increases in royalty rates** based on **sales milestones or unit thresholds**.

This concept is **not common**, but when present, it will usually:
- Appear in sections discussing **royalty rates** or **sales units**
- Include phrases indicating a **boost in royalty percentage** after surpassing a specific number of units sold

Look for phrases such as:
- "In the event that sales exceed..."
- "Upon the sale of more than X units..."
- "Royalty shall increase to X% after Y units sold"
- "Bump in royalty"
- "Escalation in rate"

This is commonly referred to as a **“bump clause”** or **royalty escalation clause** and reflects a structured incentive for high-performing sales.

If no such language is found in the document, return:
{ "field": "Bumps", "value": "Not Found" }
"""