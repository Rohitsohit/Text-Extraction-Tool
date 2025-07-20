from flask import Flask, request, jsonify
import os
import json
from docx import Document
from extractor import extract_text_from_pdf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'  # Folder where you will save the JSON files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

JSON_FILE = "field_descriptions.json"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    ext = filename.rsplit('.', 1)[-1].lower()

    if ext == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)
    #elif ext == 'docx':
        #extracted_text = extract_text_from_docx(file_path)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400


    # Save JSON to file
    output_data = {
        'filename': filename,
        'text': extracted_text  
    }

    json_filename = filename.rsplit('.', 1)[0] + '.json'
    json_path = os.path.join(OUTPUT_FOLDER, json_filename)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    return jsonify({
        'file': json_filename,
        'preview': extracted_text  
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