from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"message": "L'API fonctionne ✅"}), 200

@app.route("/api/generate", methods=["POST"])
def generate_code():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"output": "❌ Prompt manquant"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # ✅ GPT-4 Omni
            messages=[
                {"role": "system", "content": "Tu es un assistant qui génère du code clair, moderne et bien structuré."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        code = response.choices[0].message.content
        return jsonify({"output": code})
    except Exception as e:
        return jsonify({"output": f"❌ Erreur : {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
