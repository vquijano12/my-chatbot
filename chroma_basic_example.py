# import
import io
import numpy as np
import sqlite3
from langchain_community.document_loaders import TextLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# load the document and split it into chunks
loader = TextLoader("docs/state_of_the_union.txt")
documents = loader.load()

# split it into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function using HuggingFaceEmbeddings
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Database-related code starts here

# Connect to SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect("documents_embeddings.db")
c = conn.cursor()

# Create table to store documents and their embeddings
c.execute(
    """CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, document TEXT, embedding BLOB)"""
)

# Function to convert numpy array to binary for SQLite
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

# Register the conversion function
sqlite3.register_adapter(np.ndarray, adapt_array)

# Insert documents and their embeddings into the database
for doc in docs:
    doc_text = doc.page_content
    embedding = embedding_function.embed_documents([doc_text])[0]
    # Ensure embedding is a numpy array
    embedding_array = np.array(embedding)
    # Insert document chunk and embedding into the database
    c.execute(
        "INSERT INTO documents (document, embedding) VALUES (?, ?)",
        (doc_text, adapt_array(embedding_array)),
    )

# Commit the changes and close the connection
conn.commit()
conn.close()

# To perform queries, you would need to implement a function that converts
# embeddings back from binary and computes similarity with the query embedding.
# This part is not included in the snippet above.