import os
import argparse
from dotenv import load_dotenv
from .document_loader import load_documents
from .text_splitter import split_documents
from .embedding_model import embed_documents, embed_query
from .vector_store import (
    connect_db,
    create_documents_table,
    insert_document_with_embedding,
    fetch_relevant_documents,
)
from .prompt_template import get_prompt_template
from .chat_model import generate_response


def ingest(directory, db_path):
    filepaths = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]
    docs = load_documents(filepaths)
    chunks = split_documents(docs)
    embeddings = embed_documents(chunks)
    conn = connect_db(db_path)
    create_documents_table(conn)
    for chunk, embedding in zip(chunks, embeddings):
        insert_document_with_embedding(conn, chunk.page_content, embedding)
    conn.close()
    print("Ingestion complete.")


def generate(db_path):
    conn = connect_db(db_path)
    while True:
        query = input("You: ")
        if query.lower() in {"exit", "quit"}:
            break
        query_embedding = embed_query(query)
        docs = fetch_relevant_documents(conn, query_embedding)
        context = "\n\n".join(doc["content"] for doc in docs)
        prompt = get_prompt_template().format(context=context, question=query)
        answer = generate_response(prompt)
        if hasattr(answer, "content"):
            print("Bot:", answer.content)
        else:
            print("Bot:", answer)
    conn.close()


def main():
    backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(backend_root, ".env"))
    directory = os.path.join(backend_root, "raw_documents")
    db_path = os.path.join(backend_root, "vector-store", "vector_store.db")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=["ingest", "chat"],
        help="Choose 'ingest' to process documents or 'chat' to ask questions.",
    )
    args = parser.parse_args()

    if args.mode == "ingest":
        ingest(directory, db_path)
    elif args.mode == "chat":
        generate(db_path)


if __name__ == "__main__":
    main()
