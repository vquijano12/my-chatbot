import sqlite3
import json
import os
import numpy as np


def connect_db(db_path=None):
    if db_path is None:
        backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(backend_root, "vector-store", "vector_store.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def create_documents_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT UNIQUE,
            embedding TEXT
        )
        """
    )
    conn.commit()


def insert_document_with_embedding(conn, content, embedding):
    cursor = conn.cursor()
    embedding_json = json.dumps(embedding)
    cursor.execute(
        "INSERT INTO documents (content, embedding) VALUES (?, ?)",
        (content, embedding_json),
    )
    conn.commit()


def fetch_relevant_documents(conn, query_embedding, top_n=5, threshold=0.7):
    """
    Retrieves the top_n most relevant documents from the database
    based on cosine similarity to the query_embedding.
    Assumes embeddings are stored as JSON arrays (TEXT).
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, embedding FROM documents")
    rows = cursor.fetchall()

    docs = []
    similarities = []
    query_vec = np.array(query_embedding, dtype=np.float32)
    for row in rows:
        doc_id, content, embedding_json = row
        doc_vec = np.array(json.loads(embedding_json), dtype=np.float32)
        sim = np.dot(query_vec, doc_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
        )
        if sim >= threshold:
            docs.append({"id": doc_id, "content": content, "similarity": sim})
            similarities.append(sim)

    # Sort by similarity and return top_n
    top_docs = sorted(docs, key=lambda x: x["similarity"], reverse=True)[:top_n]
    return top_docs
