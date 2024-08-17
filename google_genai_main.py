import os
from google_genai_document_processing import load_and_process_documents
from google_genai_database import (
    connect_db,
    create_documents_table,
    insert_documents_with_embeddings,
)


def main():

    filepaths = [
        "docs/urban_sustainability.txt",
        "docs/urban_sustainability_case_studies.txt",
        "docs/urban_sustainability_challenges.txt",
        "docs/urban_sustainability_solutions.txt",
        "docs/urban_sustainability_technologies.txt",
        "docs/urban_sustainability_policies.txt",
    ]

    docs, embeddings = load_and_process_documents(filepaths)

    # Debugging: Print the current working directory
    print(f"Current working directory: {os.getcwd()}")

    conn = connect_db()

    # Debugging: Verify the database connection
    print(f"Database connection: {conn}")

    create_documents_table(conn)
    insert_documents_with_embeddings(conn, docs, embeddings)

    # Debugging: Verify the table creation and data insertion
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents';")
    table_exists = c.fetchone()
    if table_exists:
        print("Table 'documents' exists.")
        c.execute("SELECT COUNT(*) FROM documents;")
        count = c.fetchone()[0]
        print(f"Number of records in 'documents' table: {count}")
    else:
        print("Table 'documents' does not exist.")

    conn.close()


if __name__ == "__main__":
    main()
