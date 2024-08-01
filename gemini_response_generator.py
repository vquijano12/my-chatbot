from langchain_google_genai import ChatGoogleGenerativeAI
from google_genai_config import get_api_key
from google_genai_document_retrieval import (
    get_query_embedding,
    fetch_document_embeddings,
    get_most_relevant_documents,
)

prompt = "Provide a brief explanation of the topic in one sentence."

if __name__ == "__main__":
    api_key = get_api_key()
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    while True:  # Start an infinite loop
        # Prompt the user for a query
        query = input("Enter your query (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if query.lower() == "exit":
            print("Exiting...")
            break  # Exit the loop

        query_embedding = get_query_embedding(query, api_key)

        doc_embeddings = fetch_document_embeddings()

        top_documents_info = get_most_relevant_documents(query, api_key, top_n=5)

        if isinstance(top_documents_info, str):
            print(top_documents_info)
        else:
            context = " ".join([doc_text for _, _, doc_text in top_documents_info])

            # Append the instruction to the context
            context_with_instruction = context + prompt

            # Use the modified context to generate a response
            response = llm.invoke(context_with_instruction)

            print("Generated Response:", response.content)
