# Import necessary libraries
import time
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from google_genai_database import (
    connect_db,
    create_documents_table,
    insert_documents_with_embeddings,
)


# Define a function to load and process multiple documents
def load_and_process_documents(filepaths):
    # Connect to the database
    conn = connect_db()
    create_documents_table(conn)

    # Create instance of the GoogleGenerativeAIEmbeddings class
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    for filepath in filepaths:
        # Load the document
        loader = TextLoader(filepath)
        documents = loader.load()

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=75, chunk_overlap=30)
        docs = text_splitter.split_documents(documents)

        # Create embeddings for the chunks
        embeddings_list = [embeddings.embed_query(doc.page_content) for doc in docs]

        # Get the max doc_id from the database
        c = conn.cursor()
        c.execute("SELECT MAX(doc_id) FROM documents;")
        max_doc_id_query = c.fetchall()
        print("max_doc_id_query:", max_doc_id_query)

        int_max_doc_id_query = 0
        if max_doc_id_query[0][0] is not None:
            int_max_doc_id_query = max_doc_id_query[0][0]

        # Insert the chunks and embeddings into the database with the correct doc_id
        insert_documents_with_embeddings(
            conn, docs, embeddings_list, int_max_doc_id_query + 1
        )

        # Introduce a delay after processing the full text document
        time.sleep(1)  # Adjust the delay as needed

    # Close the database connection
    conn.close()

    if embeddings_list:
        print("Embeddings were successfully created.")
    else:
        print("Failed to create embeddings.")

    return docs, embeddings_list
