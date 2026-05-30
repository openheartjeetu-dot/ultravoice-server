from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.route("/")
def home():
    return jsonify({"status": "UltraVoice Server Running"})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    text = data.get("text")
    voice_id = data.get("voice_id")

    if not text or not voice_id:
        return jsonify({"error": "text and voice_id required"}), 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"text": text}

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    return (
        response.content,
        response.status_code,
        {"Content-Type": "audio/mpeg"}
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
