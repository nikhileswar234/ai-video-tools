from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Size limits (bytes)
MIN_SIZE = 5 * 1024 * 1024    # 5MB
MAX_SIZE = 25 * 1024 * 1024   # 25MB

@app.route("/")
def home():
    return "Backend running"

@app.route("/upload", methods=["POST"])
def upload():
    if "video" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["video"]
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size < MIN_SIZE:
        return jsonify({"error": "File too small"}), 400

    if size > MAX_SIZE:
        return jsonify({"error": "File too large"}), 400

    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)

    # Example: extract duration (light operation)
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.close()

    os.remove(video_path)

    return jsonify({
        "message": "Video processed successfully",
        "duration_seconds": duration
    })
