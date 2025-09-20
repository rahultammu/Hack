from flask import Flask, request, jsonify
from google.cloud import storage, speech
import PyPDF2
import tempfile
import os
import mimetypes
from moviepy.editor import VideoFileClip

from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech


app = Flask(__name__)

BUCKET_NAME = "startup-eval-files"  # keep it consistent

# -----------------------------
# Upload to Google Cloud Storage
# -----------------------------
def upload_to_gcs(file_obj, filename, folder="pitch_decks"):
    storage_client = storage.Client()
    bucket = storage_client.bucket("startup-eval-files")
    blob = bucket.blob(f"{folder}/{filename}")
    blob.upload_from_file(file_obj)
    return f"gs://{BUCKET_NAME}/{folder}/{filename}"

# -----------------------------
# PDF text extraction
# -----------------------------
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

# -----------------------------
# Audio transcription (MP3/WAV)
# -----------------------------
def transcribe_audio_gcs(gcs_uri, encoding="MP3", sample_rate=16000):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=getattr(speech.RecognitionConfig.AudioEncoding, encoding),
        sample_rate_hertz=sample_rate,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=300)
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcript

# -----------------------------
# Video handling (extract audio first)
# -----------------------------
def extract_audio_from_video(local_video_path, output_audio_path):
    clip = VideoFileClip(local_video_path)
    clip.audio.write_audiofile(output_audio_path, codec="mp3")

# -----------------------------
# Route: Upload + Extract
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save temporarily to detect type
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        local_path = tmp.name

    mime_type, _ = mimetypes.guess_type(file.filename)
    gcs_url = upload_to_gcs(open(local_path, "rb"), file.filename)

    extracted_text = ""

    # PDF → extract text
    if mime_type == "application/pdf":
        extracted_text = extract_text_from_pdf(local_path)

    # Audio (mp3, wav) → transcribe
    elif mime_type and mime_type.startswith("audio"):
        extracted_text = transcribe_audio_gcs(gcs_url, encoding="MP3")

    # Video (mp4, mov) → extract audio then transcribe
    elif mime_type and mime_type.startswith("video"):
        audio_path = local_path + ".mp3"
        extract_audio_from_video(local_path, audio_path)

        # Upload extracted audio to GCS
        audio_filename = file.filename.rsplit(".", 1)[0] + ".mp3"
        audio_gcs_url = upload_to_gcs(open(audio_path, "rb"), audio_filename, folder="audio_from_video")

        extracted_text = transcribe_audio_gcs(audio_gcs_url, encoding="MP3")

    else:
        extracted_text = "Unsupported file type."

    os.remove(local_path)  # cleanup

    return jsonify({
        "message": "File uploaded & processed",
        "file_url": gcs_url,
        "extracted_text": extracted_text
    })

if __name__ == "__main__":
    app.run(debug=True)
