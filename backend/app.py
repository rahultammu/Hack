import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from google.cloud import storage
from PyPDF2 import PdfReader
import speech_recognition as sr

# Flask app
app = Flask(__name__, template_folder=".")
CORS(app)

# Google Cloud Storage bucket name
BUCKET_NAME = "startup-eval-files-rahul-123"

# Upload file to GCS
def upload_to_gcs(file_obj, filename, folder="pitch_decks"):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"{folder}/{filename}")

    # Reset file pointer
    file_obj.seek(0)
    blob.upload_from_file(file_obj, content_type=file_obj.content_type)
    return f"gs://{BUCKET_NAME}/{folder}/{filename}"

# Extract text from PDF
def extract_text_from_pdf(file_obj):
    file_obj.seek(0)
    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# Extract text from audio
def extract_text_from_audio(file_obj, filename):
    file_obj.seek(0)
    temp_path = f"/tmp/{secure_filename(filename)}"

    # Save temporarily
    with open(temp_path, "wb") as f:
        f.write(file_obj.read())

    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
    except Exception:
        text = ""

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return text

# Homepage → serve index.html
@app.route("/")
def index():
    return render_template("index.html")

# Upload endpoint
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)

    # Upload to GCS
    gcs_url = upload_to_gcs(file, filename)

    # Extract text
    text = ""
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.lower().endswith((".wav", ".mp3")):
        text = extract_text_from_audio(file, filename)
    else:
        text = "File type not supported for text extraction."

    return jsonify({
        "message": "File uploaded and processed",
        "file_url": gcs_url,
        "extracted_text": text
    })

if __name__ == "__main__":
    # IMPORTANT: listen on 0.0.0.0 so Cloud Shell Web Preview can access it
    app.run(host="0.0.0.0", port=5000, debug=True)
