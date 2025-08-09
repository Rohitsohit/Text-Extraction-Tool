# Text Extraction Tool

A Flask-based API for extracting structured information from PDF documents (music royalty contracts) using OpenAI GPT and custom field logic.

## Features
- Upload PDF files and extract structured text fields
- Extract from direct file upload or from a file URL (Google Drive supported)
- Customizable field extraction using OpenAI GPT
- S3-based file storage
- Supports both local development and AWS Lambda deployment

## Requirements
- Python 3.8+
- OpenAI API key
- AWS S3 bucket configured

## Installation

### For Local Development:

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Text Extraction Tool
   ```

2. **Install local dependencies:**
   ```bash
   pip install -r requirements-local.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the project root with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Configure AWS S3:**
   - Ensure your AWS credentials are configured
   - Update the `S3_BUCKET` variable in `app.py` with your bucket name

5. **Run locally:**
   ```bash
   python app.py
   ```

### For AWS Lambda Deployment:

1. **Use the Lambda layer** (`lambda-layer-final-working.zip`) that contains all dependencies
2. **Upload the Lambda function code** (without local dependencies)
3. **Add environment variables** in Lambda console:
   - `OPENAI_API_KEY`: Your OpenAI API key

## Running the App

### Local Development:
```bash
python app.py
```
The Flask server will start on `http://127.0.0.1:5000/` by default.

### Lambda Deployment:
- Deploy using the provided Lambda layer
- Configure API Gateway for HTTP endpoints

## API Endpoints

### 1. Upload a PDF file
- **POST** `/upload`
- Form-data: `file` (PDF)
- Returns: Extracted text (file stored in S3)

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

## Development vs Production

### Local Development:
- Uses `requirements-local.txt` with `awsgi` for local testing
- Runs Flask development server
- Full debugging capabilities

### Lambda Production:
- Uses Lambda layer with `aws-wsgi` (Lambda-compatible)
- No local dependencies needed
- Optimized for serverless execution

## Notes
- Only PDF files are currently supported for extraction.
- Requires a valid OpenAI API key for GPT-based extraction.
- Files are stored in AWS S3 bucket.
- Field descriptions are stored locally in `field_descriptions.json`.
- The code automatically detects whether it's running locally or in Lambda.

## License
MIT 