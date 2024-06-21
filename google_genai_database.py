# Import necessary libraries
import sqlite3
import json


# Define a function to connect to the database
def connect_db(db_name="genai_embeddings.db"):
    # Connect to the database
    return sqlite3.connect(db_name)


def create_documents_table(conn):
    c = conn.cursor()
    # Create the table where the documents and embeddings will be stored
    c.execute(
        """CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, document TEXT, embedding TEXT)"""
    )
    conn.commit()


def insert_documents_with_embeddings(conn, docs, embeddings):
    c = conn.cursor()
    for doc, embedding in zip(docs, embeddings):
        # Convert the embedding to a JSON string
        embedding_json = json.dumps(embedding)
        # Insert the document and its embedding into the database
        c.execute(
            "INSERT INTO documents (document, embedding) VALUES (?, ?)",
            (doc.page_content, embedding_json),
        )
    conn.commit()
