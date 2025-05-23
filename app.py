# ASSEMBLYAI_API_KEY = "48a229333e45454297e34bf2586e97ed"
# OPENAI_API_KEY = "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"

from flask import Flask, request, jsonify, send_from_directory
import os
import openai
import requests
import time

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

openai.api_key = "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"
ASSEMBLYAI_API_KEY = "48a229333e45454297e34bf2586e97ed"

# Serve index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/upload", methods=["POST"])
def upload_audio():
    audio = request.files.get("audio")
    if not audio:
        return jsonify({"error": "No audio provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, "recording.wav")
    audio.save(file_path)

    # Upload to AssemblyAI
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    upload_res = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        files={'file': open(file_path, 'rb')}
    )
    audio_url = upload_res.json()['upload_url']

    # Transcribe
    transcript_req = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        json={"audio_url": audio_url},
        headers=headers
    )
    transcript_id = transcript_req.json()['id']

    # Poll
    status = 'queued'
    while status not in ['completed', 'error']:
        poll = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=headers
        ).json()
        status = poll['status']
        if status == 'completed':
            transcript = poll['text']
        elif status == 'error':
            return jsonify({"error": "Transcription failed."})
        else:
            time.sleep(1)

    # ChatGPT
    try:
        gpt_res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": transcript}]
        )
        response_text = gpt_res.choices[0].message.content.strip()
    except Exception as e:
        response_text = f"Error from GPT: {e}"

    return jsonify({
        "transcript": transcript,
        "response": response_text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
