import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_modules.gemini_response_generator import generate_response

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        if not data or "input" not in data:
            return jsonify({"error": "Invalid input"}), 400

        input_text = data["input"]
        response = generate_response(input_text)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
