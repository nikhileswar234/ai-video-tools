from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Backend running"

@app.route("/extract-audio", methods=["POST"])
def extract_audio():
    if "video" not in request.files:
        return jsonify({"error": "No file"}), 400

    video = request.files["video"]

    if video.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    audio_path = os.path.join(
        OUTPUT_FOLDER,
        os.path.splitext(video.filename)[0] + ".mp3"
    )

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()

    return jsonify({
        "success": True,
        "message": "Audio extracted successfully"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
