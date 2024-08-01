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


# Define a function to check if a document already exists in the database
def document_exists(conn, document_content):
    c = conn.cursor()
    c.execute("SELECT 1 FROM documents WHERE document = ?", (document_content,))
    return c.fetchone() is not None


# Define a function to insert documents into the database if they don't already exist
def insert_documents_with_embeddings(conn, docs, embeddings):
    c = conn.cursor()
    for doc, embedding in zip(docs, embeddings):
        if not document_exists(conn, doc.page_content):
            # Convert the embedding to a JSON string
            embedding_json = json.dumps(embedding)
            # Insert the document and its embedding into the database
            c.execute(
                "INSERT INTO documents (document, embedding) VALUES (?, ?)",
                (doc.page_content, embedding_json),
            )
    conn.commit()
