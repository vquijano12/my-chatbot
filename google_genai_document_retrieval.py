import sqlite3


def retrieve_document_and_embedding_by_id(db_path, document_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Use a parameterized query to prevent SQL injection
    cursor.execute(
        "SELECT document, embedding FROM documents WHERE id = ?", (document_id,)
    )
    result = cursor.fetchone()
    if result:
        document, embedding = result
        print("Document:", document)
        print("Embedding:", embedding)
    else:
        print("No document found with ID:", document_id)
    conn.close()


if __name__ == "__main__":
    db_path = "genai_embeddings.db"
    document_id = 1  # Example document ID
    retrieve_document_and_embedding_by_id(db_path, document_id)
