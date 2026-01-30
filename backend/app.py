from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
import cv2
from moviepy.editor import VideoFileClip
import uuid

app = Flask(__name__)
CORS(app)  # VERY IMPORTANT for frontend access

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "AI Video Tools Backend is running 🚀"

@app.route("/audio", methods=["POST"])
def extract_audio():
    video = request.files["video"]
    uid = str(uuid.uuid4())

    video_path = os.path.join(UPLOAD_FOLDER, uid + video.filename)
    audio_path = os.path.join(OUTPUT_FOLDER, uid + ".mp3")

    video.save(video_path)

    subprocess.run(
        ["ffmpeg", "-i", video_path, audio_path, "-y"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return send_file(audio_path, as_attachment=True)

@app.route("/compress", methods=["POST"])
def compress_video():
    video = request.files["video"]
    uid = str(uuid.uuid4())

    video_path = os.path.join(UPLOAD_FOLDER, uid + video.filename)
    output_path = os.path.join(OUTPUT_FOLDER, uid + "_compressed.mp4")

    video.save(video_path)

    subprocess.run(
        ["ffmpeg", "-i", video_path, "-vcodec", "libx264", "-crf", "28", output_path, "-y"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return send_file(output_path, as_attachment=True)

@app.route("/metadata", methods=["POST"])
def metadata():
    video = request.files["video"]
    path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(path)

    clip = VideoFileClip(path)
    data = {
        "duration_seconds": round(clip.duration, 2),
        "resolution": f"{clip.w}x{clip.h}",
        "fps": clip.fps
    }
    clip.close()

    return jsonify(data)

@app.route("/thumbnail", methods=["POST"])
def thumbnail():
    video = request.files["video"]
    uid = str(uuid.uuid4())

    path = os.path.join(UPLOAD_FOLDER, uid + video.filename)
    thumb_path = os.path.join(OUTPUT_FOLDER, uid + ".jpg")

    video.save(path)

    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    success, frame = cap.read()
    if success:
        cv2.imwrite(thumb_path, frame)
    cap.release()

    return send_file(thumb_path, as_attachment=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


