import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_response_generator import generate_response

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = generate_response(query)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
