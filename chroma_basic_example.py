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

# Create table to store documents and their embeddings as TEXT
c.execute(
    """CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, document TEXT, embedding TEXT)"""
)

# Function to convert numpy array to a comma-separated string
def array_to_string(arr):
    return ','.join(map(str, arr))

# Insert documents and their embeddings into the database
for doc in docs:
    doc_text = doc.page_content
    embedding = embedding_function.embed_documents([doc_text])[0]
    # Ensure embedding is a numpy array
    embedding_array = np.array(embedding)
    # Convert numpy array to a comma-separated string
    embedding_string = array_to_string(embedding_array)
    # Insert document chunk and embedding into the database
    c.execute(
        "INSERT INTO documents (document, embedding) VALUES (?, ?)",
        (doc_text, embedding_string),
    )

# Commit the changes and close the connection
conn.commit()
conn.close()

# To perform queries, you would need to implement a function that converts
# embeddings back from binary and computes similarity with the query embedding.
# This part is not included in the snippet above.