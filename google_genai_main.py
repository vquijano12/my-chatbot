from google_genai_config import get_api_key
from google_genai_document_processing import load_and_process_documents
from google_genai_database import (
    connect_db,
    create_documents_table,
    insert_documents_with_embeddings,
)


def main():
    api_key = get_api_key()

    docs, embeddings = load_and_process_documents("docs/urban_oasis.txt")

    conn = connect_db()
    create_documents_table(conn)
    insert_documents_with_embeddings(conn, docs, embeddings)
    conn.close()


if __name__ == "__main__":
    main()
