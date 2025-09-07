from langchain_google_genai import GoogleGenerativeAIEmbeddings
from .config import get_api_key


def get_embedding_model():
    api_key = get_api_key()
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )


def embed_documents(docs):
    model = get_embedding_model()
    return model.embed_documents([doc.page_content for doc in docs])


def embed_query(query):
    model = get_embedding_model()
    return model.embed_query(query)
