from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "mistralai/mistral-small-3.1-24b-instruct:free",
            "messages": [{"role": "user", "content": user_message}],
        },
    )

    reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
