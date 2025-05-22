# openai.api_key = "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"
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data or not data['message'].strip():
        return jsonify({'answer': 'Please say something.'})

    user_message = data['message']
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({'response': response['choices'][0]['message']['content'].strip()})
    except Exception as e:
        return jsonify({'error': str(e)})

