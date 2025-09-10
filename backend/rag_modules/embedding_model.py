from langchain_google_genai import GoogleGenerativeAIEmbeddings
from .config import get_api_key
import datetime
import time


def log_embedding_usage(query):
    with open("embedding_usage.log", "a") as log_file:
        log_file.write(
            f"{datetime.datetime.now().isoformat()} | {len(query)} chars | {query[:50]}...\n"
        )


def get_embedding_model():
    api_key = get_api_key()
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", google_api_key=api_key
    )


def embed_documents(docs, delay=0.75):  # delay in seconds (e.g., 0.5s = 2 requests/sec)
    model = get_embedding_model()
    embeddings = []
    for doc in docs:
        log_embedding_usage(doc.page_content)
        embedding = model.embed_documents([doc.page_content])[0]
        embeddings.append(embedding)
        time.sleep(delay)  # Add delay between requests
    return embeddings


def embed_query(query):
    log_embedding_usage(query)
    model = get_embedding_model()
    return model.embed_query(query)
