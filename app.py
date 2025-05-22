# openai.api_key = "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"
import os
import time
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()
ASSEMBLYAI_API_KEY = "48a229333e45454297e34bf2586e97ed"
OPENAI_API_KEY = "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"

# ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

# Upload audio file to AssemblyAI
def upload_audio(file_url):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    response = requests.post("https://api.assemblyai.com/v2/transcript", json={"audio_url": file_url}, headers=headers)
    return response.json()['id']

# Poll for transcription result
def poll_transcription(transcript_id):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    while True:
        response = requests.get(polling_endpoint, headers=headers).json()
        if response['status'] == 'completed':
            return response['text']
        elif response['status'] == 'error':
            raise Exception(response['error'])
        time.sleep(2)

# ChatGPT interaction
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

@app.route("/voice-chat", methods=["POST"])
def voice_chat():
    data = request.get_json()
    audio_url = data.get("audio_url")
    if not audio_url:
        return jsonify({"error": "Missing 'audio_url' in request"}), 400

    try:
        transcript_id = upload_audio(audio_url)
        transcript = poll_transcription(transcript_id)
        answer = chat_with_gpt(transcript)
        return jsonify({
            "transcript": transcript,
            "response": answer
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "AssemblyAI + ChatGPT voice chatbot is live!"

