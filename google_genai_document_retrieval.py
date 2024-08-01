# Import necessary libraries
import os
import json
import sqlite3
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from google_genai_config import get_api_key


def get_query_embedding(query, api_key):
    # Create an instance of the GoogleGenerativeAIEmbeddings class
    embeddings_generator = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )
    # Generate the embedding for the query
    return embeddings_generator.embed_query(query)


def fetch_document_embeddings():
    # Connect to the database
    conn = sqlite3.connect("genai_embeddings.db")
    c = conn.cursor()
    # Retrieve all document IDs, their embeddings, and the actual document content from the database
    c.execute("SELECT id, embedding, document FROM documents")
    # Convert the fetched data into a dictionary: each document's ID is mapped to its embedding and content
    embeddings = {row[0]: (json.loads(row[1]), row[2]) for row in c.fetchall()}
    conn.close()
    return embeddings


# Define the relevance threshold as a constant
RELEVANCE_THRESHOLD = 0.7


def calculate_similarity(query_embedding, doc_embeddings):
    query_emb_array = np.array(query_embedding).reshape(1, -1)
    doc_info = []

    # Iterate over the document embeddings
    for doc_id, (doc_embedding, doc_text) in doc_embeddings.items():
        # Convert the document embedding to a numpy array
        doc_emb_array = np.array(doc_embedding).reshape(1, -1)
        # Calculate the cosine similarity between the query and document embeddings
        similarity = cosine_similarity(query_emb_array, doc_emb_array)[0][0]
        # Check if the similarity is above the relevance threshold
        if similarity >= RELEVANCE_THRESHOLD:
            # Append the document ID, similarity score, and document text to the list
            doc_info.append((doc_id, similarity, doc_text))
    return doc_info


def get_most_relevant_documents(query, api_key, top_n=5):
    # Generate the embedding for the query
    query_embedding = get_query_embedding(query, api_key)

    # Retrieve the document embeddings from the database
    doc_embeddings = fetch_document_embeddings()

    # Calculate the similarity between the query and document embeddings
    doc_info = calculate_similarity(query_embedding, doc_embeddings)

    # Sort the documents by similarity score in descending order and select the top N documents
    sorted_doc_info = sorted(doc_info, key=lambda x: x[1], reverse=True)[:top_n]

    # Check if any documents meet the relevance threshold
    if not sorted_doc_info:
        return "Sorry, I cannot help with that."

    return sorted_doc_info


# if __name__ == "__main__":
#     api_key = get_api_key()

#     query = "Tell me about urban sustainability."
#     top_documents_info = get_most_relevant_documents(query, api_key)
#     for doc_id, similarity, doc_text in top_documents_info:
#         print(f"Document ID: {doc_id}, Similarity: {similarity}")
#         print(f"Document Text: {doc_text}\n")
#         # print(f"Embedding: {embedding}\n")
