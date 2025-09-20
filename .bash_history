gcloud config set project [PROJECT_ID]
gcloud config set project sylvan-box-471410-j3
gcloud services enable   run.googleapis.com   artifactregistry.googleapis.com   cloudbuild.googleapis.com
ls
cat pyproject.toml
uv add fastmcp==2.11.1 --no-sync
cloudshell edit server.py
cloudshell edit Dockerfile
gcloud run deploy zoo-mcp-server     --no-allow-unauthenticated     --region=europe-west1     --source=.     --labels=dev-tutorial=codelab-mcp
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT     --member=user:$(gcloud config get-value account)     --role='roles/run.invoker'
export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
export ID_TOKEN=$(gcloud auth print-identity-token)
cloudshell edit ~/.gemini/settings.json
gemini
ls
gcloud config set project sylvan-box-471410-j3
gcloud services enable storage.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable documentai.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable gmail.googleapis.com
gcloud services enable customsearch.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
# create a bucket (name must be globally unique)
gsutil mb -l asia-south1 gs://startup-eval-files/
# folders inside bucket (not real folders, but prefixes)
gsutil cp pitch_deck.pdf gs://startup-eval-files/raw/pitchdecks/
gsutil cp founder_call.mp3 gs://startup-eval-files/raw/calls/
gsutil cp emails.txt gs://startup-eval-files/raw/emails/
gsutil mb -l asia-south1 gs://startup-eval-files/
gsutil cp pitch_deck.pdf gs://startup-eval-files/raw/pitchdecks/
ls
pip install flask google-cloud-storage
from flask import Flask, request, jsonify
from google.cloud import storage
import os
app = Flask(__name__)
# Make sure you set GOOGLE_APPLICATION_CREDENTIALS to your service account JSON
BUCKET_NAME = "startup-data-pipeline"
def upload_to_gcs(file_obj, filename, folder="pitch_decks"):
@app.route("/upload", methods=["POST"])
def upload_file():
if __name__ == "__main__":;     app.run(debug=True)
create app.py
gcloud config set project sylvan-box-471410-j3
gcloud services enable storage.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable documentai.googleapis.com
# enable speech-to-text (for calls)
gcloud services enable speech.googleapis.com
# enable Vertex AI (summarization, structuring)
gcloud services enable aiplatform.googleapis.com
# optional: Gmail API (for emails)
gcloud services enable gmail.googleapis.com
# optional: Custom Search API (for news/public data)
gcloud services enable customsearch.googleapis.com
gsutil mb -l asia-south1 gs://startup-eval-files/
gs://startup-data-pipeline/pitch_decks/yourfile.pdf
gs://startup-data-pipeline/pitch_decks/
ls
gs://startup-data-pipeline/pitch_decks/Jetlearn_Design_VFinal.pdf
gsutil ls
gsutil ls -l gs://startup-eval-files/pitch_decks
python app.py
run app.py
pip install google-cloud-speech
pip show google-cloud-speech
from google.cloud import speech
python app.py
pip install -r requirements.txt
sudo apt-get update
sudo apt-get install -y ffmpeg
python app.py
pip install moviepy
pip show moviepy
sudo apt-get update
sudo apt-get install -y ffmpeg
python
python app.py
pip install google-cloud-aiplatform
python app.py
export GOOGLE_APPLICATION_CREDENTIALS="/home/rahultammu71/keys/service-account.json"
export GOOGLE_APPLICATION_CREDENTIALS=/home/rahultammu71/ai-analyst-471818-9079dd0d6186.json
gcloud auth activate-service-account --key-file=/home/rahultammu71/keys/service-account.json
gcloud auth list
gcloud auth activate-service-account --key-file=/home/rahultammu71/ai-analyst-471818-9079dd0d6186.json
gcloud auth list
gcloud config set account `ACCOUNT`
gcloud config set account rahultammu71@gmail.com\
gcloud config set account rahultammu71@gmail.com
python app.py
gsutil ls
gsutil ls
gsutil mb -l us-central1 gs://startup-eval-files/
gcloud config set project ai-analyst-471818
gsutil ls
gsutil mb -l us-central1 gs://startup-eval-files/
# Replace with your project ID and service account email
PROJECT_ID="ai-analyst-471818"
SERVICE_ACCOUNT="rahul-770@ai-analyst-471818.iam.gserviceaccount.com"
# Pick a unique bucket name (must be globally unique)
BUCKET_NAME="startup-eval-files-rahul-123"
REGION="us-central1"
# Replace with your project ID and service account email
PROJECT_ID="ai-analyst-471818"
SERVICE_ACCOUNT="rahul-770@ai-analyst-471818.iam.gserviceaccount.com"
# Pick a unique bucket name (must be globally unique)
BUCKET_NAME="startup-eval-files-rahul-123"
REGION="us-central1"
gcloud config set project ai-analyst-471818
gsutil mb -l $REGION gs://$BUCKET_NAME/
gsutil iam ch serviceAccount:$SERVICE_ACCOUNT:objectCreator gs://$BUCKET_NAME
gsutil ls -L gs://$BUCKET_NAME
python app.py
pip install flask google-cloud-storage PyPDF2 SpeechRecognition moviepy pydub werkzeug
export GOOGLE_APPLICATION_CREDENTIALS="/home/rahultammu71/ai-analyst-471818-9079dd0d6186.json"
python app.py
pip install -r requirements.txt
pip install --upgrade pip
pip install -r requirements.txt --user
python app.py
pip install moviepy
pip install --upgrade pip
pip install moviepy imageio imageio-ffmpeg
python app.py
code.
.
code 
gcloud config set project ai-analyst-471818
python app.py
gcloud config set project ai-analyst-471818
python app.py
lsof -i :5000
python app.py
flask run -p 8000
gcloud config set project ai-analyst-471818
python app.py
flask run -p 8000
gcloud config set project ai-analyst-471818
gemini; exit
gcloud config set project ai-analyst-471818
python app.py
chmod 644 /home/rahultammu71/ai-analyst-471818-9079dd0d6186.json
python app.py
gemini; exit
gcloud config set project ai-analyst-471818
python app.py
gemini cli
gemini
ls
mkdir ai-analyst
cd ai-alanlyst
cd ai-analyst
gemini
ls
gemini
/home/rahultammu71/.gemini/settings.json
cd /home/rahultammu71/.gemini/settings.json
gemini; exit
gcloud config set project ai-analyst-471818
