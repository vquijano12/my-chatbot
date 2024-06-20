import io
import numpy as np
import sqlite3
from langchain_community.document_loaders import TextLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("docs/state_of_the_union.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
docs = text_splitter.split_documents(documents)

embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

conn = sqlite3.connect("documents_embeddings.db")
c = conn.cursor()


c.execute(
    """CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, document TEXT, embedding TEXT)"""
)


def array_to_string(arr):
    return ",".join(map(str, arr))


for doc in docs:
    doc_text = doc.page_content
    embedding = embedding_function.embed_documents([doc_text])[0]

    embedding_array = np.array(embedding)

    embedding_string = array_to_string(embedding_array)

    c.execute(
        "INSERT INTO documents (document, embedding) VALUES (?, ?)",
        (doc_text, embedding_string),
    )


conn.commit()
conn.close()
