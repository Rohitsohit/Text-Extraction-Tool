# Text Extraction Tool

A Flask-based API for extracting structured information from PDF documents (music royalty contracts) using OpenAI GPT and custom field logic.

## Features
- Upload PDF files and extract structured text fields
- Extract from direct file upload or from a file URL (Google Drive supported)
- Customizable field extraction using OpenAI GPT

## Requirements
- Python 3.8+
- OpenAI API key

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Text Extraction Tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the project root with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Create required folders:**
   - The app will automatically create `uploads/` and `output/` folders if they do not exist.

## Running the App

```bash
python app.py
```

The Flask server will start on `http://127.0.0.1:5000/` by default.

## API Endpoints

### 1. Upload a PDF file
- **POST** `/upload`
- Form-data: `file` (PDF)
- Returns: Extracted text and output JSON filename

### 2. Extract from a file URL
- **POST** `/extract_from_url`
- JSON body: `{ "url": "<file_url>" }`
- Returns: Extracted text

### 3. Get field descriptions
- **GET** `/get_fields`
- Returns: JSON of all field descriptions

### 4. Add or update a field description
- **POST** `/add_field`
- JSON body: `{ "field": "Field Name", "value": "Description" }`

### 5. Delete a field description
- **DELETE** `/delete_field/<field_key>`

## Notes
- Only PDF files are currently supported for extraction.
- Requires a valid OpenAI API key for GPT-based extraction.
- Output JSON files are saved in the `output/` directory.

## License
MIT 