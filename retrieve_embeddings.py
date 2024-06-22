import os
import json
import sqlite3
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

from google_genai_config import get_api_key


def get_query_embedding(query, api_key):
    embeddings_generator = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )
    return embeddings_generator.embed_query(query)


def fetch_document_embeddings():
    conn = sqlite3.connect("genai_embeddings.db")
    c = conn.cursor()
    # Fetch the document text as well
    c.execute("SELECT id, embedding, document FROM documents")
    embeddings = {row[0]: (json.loads(row[1]), row[2]) for row in c.fetchall()}
    conn.close()
    return embeddings


def calculate_similarity(query_embedding, doc_embeddings):
    query_emb_array = np.array(query_embedding).reshape(1, -1)
    doc_info = []  # This will store tuples of (doc_id, similarity, doc_text)
    for doc_id, (doc_embedding, doc_text) in doc_embeddings.items():
        doc_emb_array = np.array(doc_embedding).reshape(1, -1)
        similarity = cosine_similarity(query_emb_array, doc_emb_array)[0][0]
        doc_info.append((doc_id, similarity, doc_text))  # Include doc_text here
    return doc_info


def get_most_relevant_documents(query, api_key, top_n=2):
    query_embedding = get_query_embedding(query, api_key)
    doc_embeddings = fetch_document_embeddings()
    doc_info = calculate_similarity(query_embedding, doc_embeddings)
    # Sort based on similarity and select top N
    sorted_doc_info = sorted(doc_info, key=lambda x: x[1], reverse=True)[:top_n]
    # Return a list of tuples or a dictionary as needed
    return sorted_doc_info


if __name__ == "__main__":
    api_key = get_api_key()

    query = "the city"
    top_documents_info = get_most_relevant_documents(query, api_key)
    for doc_id, similarity, doc_text in top_documents_info:
        print(f"Document ID: {doc_id}, Similarity: {similarity}")
        print(f"Document Text: {doc_text}\n")  # Print the document text
        # print(f"Embedding: {embedding}\n")
