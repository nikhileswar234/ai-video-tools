from flask import Flask, request, jsonify
from flask_cors import CORS
from moviepy.editor import VideoFileClip
import os

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
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    clip = VideoFileClip(video_path)
    audio_path = os.path.join(OUTPUT_FOLDER, "audio.mp3")
    clip.audio.write_audiofile(audio_path)
    clip.close()

    return jsonify({"message": "Audio extracted successfully"})

if __name__ == "__main__":
    app.run()
