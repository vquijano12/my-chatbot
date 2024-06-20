import os
import json
import sqlite3
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


def get_query_embedding(query, api_key):
    embeddings_generator = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )
    return embeddings_generator.embed_query(query)


def fetch_document_embeddings():
    conn = sqlite3.connect("genai_embeddings.db")
    c = conn.cursor()
    c.execute("SELECT id, embedding FROM documents")
    embeddings = {row[0]: json.loads(row[1]) for row in c.fetchall()}
    conn.close()
    return embeddings


def calculate_similarity(query_embedding, doc_embeddings):
    query_emb_array = np.array(query_embedding).reshape(1, -1)
    doc_ids, similarities = [], []
    for doc_id, doc_embedding in doc_embeddings.items():
        doc_emb_array = np.array(doc_embedding).reshape(1, -1)
        similarity = cosine_similarity(query_emb_array, doc_emb_array)[0][0]
        doc_ids.append(doc_id)
        similarities.append(similarity)
    return doc_ids, similarities


def get_most_relevant_documents(query, api_key, top_n=5):
    query_embedding = get_query_embedding(query, api_key)
    doc_embeddings = fetch_document_embeddings()
    doc_ids, similarities = calculate_similarity(query_embedding, doc_embeddings)
    sorted_doc_ids = [
        doc for _, doc in sorted(zip(similarities, doc_ids), reverse=True)
    ]
    return sorted_doc_ids[:top_n]


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set GOOGLE_GENAI_API_KEY in the .env file."
        )

    query = "Your search query here"
    top_documents = get_most_relevant_documents(query, api_key)
    print("Top document IDs based on query:", top_documents)
