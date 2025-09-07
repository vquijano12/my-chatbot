import sys
import os
import nest_asyncio

nest_asyncio.apply()
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_modules.embedding_model import embed_query
from rag_modules.vector_store import connect_db, fetch_relevant_documents
from rag_modules.prompt_template import get_prompt_template
from rag_modules.chat_model import generate_response

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
        db_path = os.path.join(
            os.path.dirname(__file__), "vector-store", "vector_store.db"
        )

        # Modular RAG pipeline:
        conn = connect_db(db_path)
        query_embedding = embed_query(input_text)
        docs = fetch_relevant_documents(conn, query_embedding)
        context = "\n\n".join(doc["content"] for doc in docs)
        prompt = get_prompt_template().format(context=context, question=input_text)
        response = generate_response(prompt)
        conn.close()

        # Extract only the text if needed
        if hasattr(response, "content"):
            response = response.content

        return jsonify({"response": response}), 200
    except Exception as e:
        print("Error in /generate:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
