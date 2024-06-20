# Import necessary libraries
import io
import numpy as np
import sqlite3
from langchain_community.document_loaders import TextLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the text from the file
loader = TextLoader("docs/state_of_the_union.txt")
documents = loader.load()

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
docs = text_splitter.split_documents(documents)

# Create an instance of the HuggingFaceEmbeddings class
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to the database
conn = sqlite3.connect("documents_embeddings.db")
c = conn.cursor()

# Create the table where the documents and embeddings will be stored
c.execute(
    """CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, document TEXT, embedding TEXT)"""
)


# Function to convert an array to a string
def array_to_string(arr):
    return ",".join(map(str, arr))


# Loop through the documents
for doc in docs:
    # Extract the text from the document
    doc_text = doc.page_content
    # Generate the embedding for the document
    embedding = embedding_function.embed_documents([doc_text])[0]
    # Convert 'embedding' to a numpy array
    embedding_array = np.array(embedding)
    # Convert the embedding array to a string
    embedding_string = array_to_string(embedding_array)
    # Insert the document and its embedding into the database
    c.execute(
        "INSERT INTO documents (document, embedding) VALUES (?, ?)",
        (doc_text, embedding_string),
    )

# Commit the changes and close the connection
conn.commit()
conn.close()
