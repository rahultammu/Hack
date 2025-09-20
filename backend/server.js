const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { Storage } = require("@google-cloud/storage");

const app = express();
const PORT = 5000;

// Enable CORS (for frontend)
app.use(cors());

// Google Cloud Storage setup
const storage = new Storage({
  keyFilename: path.join(__dirname, "ai-analyst-471818-9079dd0d6186.json"), // your service account
});
const bucketName = "startup-eval-files-rahul-123";
const bucket = storage.bucket(bucketName);

// Multer config (temp local upload before pushing to GCS)
const upload = multer({ dest: "uploads/" });

// Upload endpoint
app.post("/upload", upload.single("file"), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ success: false, message: "No file uploaded" });
  }

  try {
    const gcsFileName = Date.now() + "-" + req.file.originalname;
    const gcsFile = bucket.file(`pitch_decks/${gcsFileName}`);

    await bucket.upload(req.file.path, {
      destination: gcsFile,
      contentType: req.file.mimetype,
    });

    // Cleanup local file
    fs.unlinkSync(req.file.path);

    res.json({
      success: true,
      message: "File uploaded to GCS successfully",
      gcsUrl: `gs://${bucketName}/pitch_decks/${gcsFileName}`,
      publicUrl: `https://storage.googleapis.com/${bucketName}/pitch_decks/${gcsFileName}`,
    });
  } catch (err) {
    console.error("Upload error:", err);
    res.status(500).json({ success: false, message: "Upload failed", error: err.message });
  }
});

// Serve uploaded files statically (not needed if always uploading to GCS)
app.use("/uploads", express.static(path.join(__dirname, "uploads")));

app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
