# Import necessary libraries
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Define a function to load and process multiple documents
def load_and_process_documents(filepaths):
    all_documents = []

    # Load and process each document
    for filepath in filepaths:
        loader = TextLoader(filepath)
        documents = loader.load()
        all_documents.extend(documents)

    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=75, chunk_overlap=30)
    docs = text_splitter.split_documents(all_documents)

    # Create instance of the GoogleGenerativeAIEmbeddings class
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create embeddings for the documents
    embeddings = [embeddings.embed_query(doc.page_content) for doc in docs]

    if embeddings:
        print("Embeddings were successfully created.")
    else:
        print("Failed to create embeddings.")

    return docs, embeddings
