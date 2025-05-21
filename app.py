from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow mobile app to access

openai.api_key = "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"

@app.route("/chat", methods=["POST"])
def chat():
    question = request.json.get("question", "")
    if not question.strip():
        return jsonify({"answer": "Please say something."})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
