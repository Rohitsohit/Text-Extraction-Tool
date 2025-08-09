import awsgi
from flask import Flask, request, jsonify
import json
import boto3
import requests
import tempfile
from extractor import extract_text_from_document,extract_text_from_pdf
from flask_cors import CORS
import os, tempfile, mimetypes
from botocore.exceptions import NoCredentialsError, ClientError
import hashlib
app = Flask(__name__)
CORS(app)

# S3 configuration
S3_BUCKET = 'extract-tool'  # Replace with your actual bucket name
s3 = boto3.client('s3')

JSON_FILE = "field_descriptions.json"

ALLOWED_EXTS = {"pdf"}
ALLOWED_MIME = {"application/pdf"}

@app.route('/extract', methods=['POST'])
def uploads():
    print("[DEBUG] /extract called")
    
    if 'file' not in request.files:
        print("[ERROR] No file found in request")
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename:
        print("[ERROR] No filename provided")
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    ext = filename.rsplit('.', 1)[-1].lower()
    print(f"[DEBUG] Received file: {filename} (ext={ext})")

    if ext not in ALLOWED_EXTS:
        print(f"[ERROR] Unsupported extension: {ext}")
        return jsonify({'error': 'Unsupported file type'}), 400

    guessed_mime = mimetypes.guess_type(filename)[0] or ""
    print(f"[DEBUG] Guessed MIME type: {guessed_mime}")
    if guessed_mime and guessed_mime not in ALLOWED_MIME:
        print(f"[ERROR] Unsupported MIME type: {guessed_mime}")
        return jsonify({'error': 'Unsupported content type'}), 400

    tmp_path = None
    try:
        # Upload to S3
        print(f"[DEBUG] Uploading to S3: bucket={S3_BUCKET}, key={filename}")
        s3.upload_fileobj(file, S3_BUCKET, filename)
        print("[DEBUG] Upload complete")

        # Download to /tmp
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + ext) as tmp:
            tmp_path = tmp.name
        print(f"[DEBUG] Temporary file path: {tmp_path}")

        s3.download_file(S3_BUCKET, filename, tmp_path)
        size_on_disk = os.path.getsize(tmp_path)
        print(f"[DEBUG] Download complete. File size: {size_on_disk} bytes")

        # >>> ETag / MD5 sanity check (prove bytes match what S3 has)
        try:
            etag = s3.head_object(Bucket=S3_BUCKET, Key=filename)["ETag"].strip('"')
        except ClientError as e:
            print("[ERROR] head_object failed:", e)
            etag = None

        with open(tmp_path, "rb") as f:
            data = f.read()
        md5 = hashlib.md5(data).hexdigest()
        print(f"[DEBUG] Size={len(data)} MD5(localcalc)={md5} S3_ETag={etag}")
        # Note: For multi-part uploads ETag != MD5, but for small single-part PDFs they should match.

        # Peek at first bytes
        head = data[:64]
        print(f"[DEBUG] First 64 bytes: {head!r}")

        # Extract text
        extracted_text = extract_text_from_document(tmp_path)
        print("[DEBUG] Text extraction complete")

        return jsonify({'file': filename, 'preview': extracted_text})

    except NoCredentialsError:
        print("[ERROR] S3 credentials not found")
        return jsonify({'error': 'S3 credentials not found'}), 500
    except ClientError as e:
        print(f"[ERROR] AWS ClientError: {e}")
        return jsonify({'error': f'AWS error: {e}'}), 500
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return jsonify({'error': f'Unexpected error: {e}'}), 500
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
                print(f"[DEBUG] Removed temporary file: {tmp_path}")
            except Exception as e:
                print(f"[WARN] Failed to remove temp file: {e}")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    
    ext = filename.rsplit('.', 1)[-1].lower()

        # Upload file to S3
    try:
        s3.upload_fileobj(file, S3_BUCKET, filename)
    except NoCredentialsError:
        return jsonify({'error': 'S3 credentials not found'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to upload to S3: {str(e)}'}), 500

    # Download from S3 to temp file for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + ext) as tmp:
        try:
            s3.download_file(S3_BUCKET, filename, tmp.name)
        except Exception as e:
            return jsonify({'error': f'Failed to download from S3: {str(e)}'}), 500
        tmp_path = tmp.name



    if ext == 'pdf':
        # extracted_text = "file saved in s3"
        extracted_text = extract_text_from_pdf(tmp_path)
    #elif ext == 'docx':
        #extracted_text = extract_text_from_docx(file_path)
    else:
        os.remove(tmp_path)
        return jsonify({'error': 'Unsupported file type'}), 400

    os.remove(tmp_path)
    

    return jsonify({
        'file': filename,
        'preview': extracted_text  
    })





# Extract text from file URL endpoint
@app.route('/extract_from_url', methods=['POST'])
def extract_from_url():
    data = request.get_json()
    file_url = data.get('url')
    

    if not file_url:
        return jsonify({'error': 'No URL provided'}), 200
    

        
    if "drive.google.com" in file_url and "/file/d/" in file_url:
        try:
            file_id = file_url.split("/file/d/")[1].split("/")[0]
            file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        except Exception:
            return jsonify({'error': 'Failed to parse Google Drive link'}), 400


    try:
        response = requests.get(file_url)
       
        response.raise_for_status()
    except Exception as e:
        return jsonify({'error': f'Failed to download file: {str(e)}'}), 200

    print("******************** : ",response.raise_for_status()," :****************")

    ext = file_url.split('.')[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + ext) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    if ext == 'pdf':
        extracted_text = extract_text_from_pdf(tmp_path)
    #elif ext == 'docx':
        #extracted_text = extract_text_from_docx(tmp_path)
    else:
        return jsonify({'error': 'Unsupported file type'}), 200

    os.remove(tmp_path)

    return jsonify({
        'url': file_url,
        'text': extracted_text
    })

@app.route("/get_fields", methods=["GET"])
def get_fields():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route("/add_field", methods=["POST"])
def update_field():
    data = request.get_json()
    field = data.get("field")
    value = data.get("value")
    print(data)
    if not field or not value:
        return jsonify({"error": "Missing 'field' or 'value'"}), 400

    # Load existing data
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            json_data = json.load(f)
    else:
        json_data = {}

    # Update field
    json_data[field] = value

    # Save back to file
    with open(JSON_FILE, "w") as f:
        json.dump(json_data, f, indent=4)

    return jsonify({"message": "Field updated successfully"}), 200

@app.route("/delete_field/<field_key>", methods=["DELETE"])
def delete_field(field_key):
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            json_data = json.load(f)
    else:
        return jsonify({"error": "File not found"}), 404

    if field_key not in json_data:
        return jsonify({"error": "Field not found"}), 404

    del json_data[field_key]

    with open(JSON_FILE, "w") as f:
        json.dump(json_data, f, indent=4)

    return jsonify({"message": f"Field '{field_key}' deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)


# def lambda_handler(event, context):
#     # Handle different event types
#     if 'httpMethod' in event:
#         # API Gateway event
#         return awsgi.response(app, event, context)
#     elif 'Records' in event:
#         # S3 or other AWS service event
#         return {
#             'statusCode': 200,
#             'body': 'Event processed successfully'
#         }
#     else:
#         # Simple test event or other event type
#         return {
#             'statusCode': 200,
#             'body': 'Lambda function is working! Use API Gateway to access the endpoints.',
#             'headers': {
#                 'Content-Type': 'application/json'
#             }
#         }