from google.cloud import vision, bigquery

# Set your bucket image path
gcs_image_uri = "gs://my-receipts-bucket2/sample_image.png"

# Initialize Vision client
vision_client = vision.ImageAnnotatorClient()
image = vision.Image()
image.source.image_uri = gcs_image_uri

# Run label detection (can also do text detection, logos, etc.)
response = vision_client.label_detection(image=image)
labels = response.label_annotations

# Print results
print("Labels found:")
for label in labels:
    print(f"{label.description} (score: {label.score:.2f})")

# Initialize BigQuery client
bq_client = bigquery.Client()
dataset_id = "my_dataset"        # Change this
table_id = "image_labels"        # Change this

# Reference table
table_ref = bq_client.dataset(dataset_id).table(table_id)
table = bq_client.get_table(table_ref)

# Insert rows
rows_to_insert = [
    {"image": gcs_image_uri, "label": label.description, "score": label.score}
    for label in labels
]

errors = bq_client.insert_rows_json(table, rows_to_insert)
if errors == []:
    print("Data successfully inserted into BigQuery ✅")
else:
    print("Errors:", errors)
