from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TOXIC_MODEL = os.getenv("TOXIC_MODEL_KEY")
TOXIC_MODEL_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

@app.route("/analyze-text", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }
        api_response = requests.post(
            f"{TOXIC_MODEL_URL}?key={TOXIC_MODEL}", json=payload
        )
        api_data = api_response.json()
        toxicity_score = api_data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return jsonify({"toxicityScore": toxicity_score})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
