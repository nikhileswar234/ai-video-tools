from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "AI Video Tools Backend Running"

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    url = data.get("url")
    action = data.get("action")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if action == "metadata":
        return jsonify({
            "title": info.get("title"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "views": info.get("view_count")
        })

    if action == "thumbnail":
        return jsonify({
            "thumbnail_url": info.get("thumbnail")
        })

    if action == "audio":
        return jsonify({
            "message": "Audio extraction can be enabled with download=True"
        })

    return jsonify({"error": "Invalid action"})
