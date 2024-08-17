from langchain_google_genai import ChatGoogleGenerativeAI
from google_genai_config import get_api_key
from google_genai_document_retrieval import (
    get_query_embedding,
    fetch_document_embeddings,
    get_most_relevant_documents,
)

prompt = "Provide a brief explanation of the topic in a small paragraph."

api_key = get_api_key()
llm = ChatGoogleGenerativeAI(model="gemini-pro")
previous_responses = []


def generate_response(query):
    top_documents_info = get_most_relevant_documents(query, api_key, top_n=5)

    if isinstance(top_documents_info, str):
        return top_documents_info
    else:
        context = " ".join([doc_text for _, _, doc_text in top_documents_info])
        combined_context = " ".join(previous_responses) + " " + context + prompt
        response = llm.invoke(combined_context)
        previous_responses.append(response.content)

        if len(previous_responses) > 5:
            previous_responses.pop(0)

        return response.content
