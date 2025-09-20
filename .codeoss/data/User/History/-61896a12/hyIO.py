from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from google.cloud import storage
from PyPDF2 import PdfReader
import os
import speech_recognition as sr


# Flask app
app = Flask(__name__)

# Google Cloud Storage bucket name
BUCKET_NAME = "your-bucket-name"  # Replace with your bucket

# Upload file to GCS
def upload_to_gcs(file_obj, filename, folder="uploads"):
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

# Extract text from audio/video
def extract_text_from_audio(file_obj, filename):
    file_obj.seek(0)
    temp_path = f"/tmp/{secure_filename(filename)}"

    # Save temporarily
    with open(temp_path, "wb") as f:
        f.write(file_obj.read())

    # Convert video to audio if needed
    if filename.lower().endswith((".mp4", ".mov", ".avi")):
        clip = VideoFileClip(temp_path)
        audio_path = f"/tmp/{secure_filename(filename)}.wav"
        clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
        temp_path = audio_path

    # Recognize speech
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    except sr.RequestError:
        text = ""

    # Clean up temp files
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return text

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Route for file upload
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
    elif filename.lower().endswith((".wav", ".mp3", ".mp4", ".mov", ".avi")):
        text = extract_text_from_audio(file, filename)
    else:
        text = "File type not supported for text extraction."

    return jsonify({
        "message": "File uploaded and processed",
        "file_url": gcs_url,
        "extracted_text": text
    })

if __name__ == "__main__":
    app.run(debug=True)
