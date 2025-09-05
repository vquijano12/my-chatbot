# Import necessary libraries
import sqlite3
import json


# Define a function to connect to the database
import os


def connect_db(db_name=None):
    if db_name is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_name = os.path.join(script_dir, "vector-store", "genai_embeddings.db")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_name), exist_ok=True)
    return sqlite3.connect(db_name)


def create_documents_table(conn):
    c = conn.cursor()
    # Create the table where the documents and embeddings will be stored
    c.execute(
        """CREATE TABLE IF NOT EXISTS documents
                 (id INTEGER PRIMARY KEY, document TEXT, embedding TEXT, doc_id INTEGER)"""
    )
    # Check if the doc_id column exists
    c.execute("PRAGMA table_info(documents);")
    columns = [column[1] for column in c.fetchall()]
    if "doc_id" not in columns:
        # Add the doc_id column if it doesn't exist
        c.execute("ALTER TABLE documents ADD COLUMN doc_id INTEGER")
    conn.commit()


# Define a function to check if a document already exists in the database
def document_exists(conn, document_content):
    c = conn.cursor()
    c.execute("SELECT 1 FROM documents WHERE document = ?", (document_content,))
    return c.fetchone() is not None


# Define a function to insert documents into the database if they don't already exist
def insert_documents_with_embeddings(conn, docs, embeddings, doc_id):
    c = conn.cursor()
    for doc, embedding in zip(docs, embeddings):
        if not document_exists(conn, doc.page_content):
            # Convert the embedding to a JSON string
            embedding_json = json.dumps(embedding)
            # Insert the document and its embedding into the database with the doc_id
            c.execute(
                "INSERT INTO documents (document, embedding, doc_id) VALUES (?, ?, ?)",
                (doc.page_content, embedding_json, doc_id),
            )
    conn.commit()
