# Import necessary libraries
import os
import json
import sqlite3
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import HarmBlockThreshold, HarmCategory

# Load all the variables found as environment variables in the .env file
load_dotenv()
# Get the API key from the .env file
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set GOOGLE_GENAI_API_KEY in the .env file."
    )

# Load the text from the file
loader = TextLoader("docs/urban_oasis.txt")
documents = loader.load()

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
docs = text_splitter.split_documents(documents)

# Create instance of the GoogleGenerativeAIEmbeddings class
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create embeddings for the documents
embeddings = [embeddings.embed_query(doc.page_content) for doc in docs]

# Connect to the database
conn = sqlite3.connect("genai_embeddings.db")
c = conn.cursor()
# Create the table where the documents and embeddings will be stored
c.execute(
    """CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, document TEXT, embedding TEXT)"""
)

for doc, embedding in zip(docs, embeddings):
    # Convert the embedding to a JSON string
    embedding_json = json.dumps(embedding)
    # Insert the document and its embedding into the database
    c.execute(
        "INSERT INTO documents (document, embedding) VALUES (?, ?)",
        (doc.page_content, embedding_json),
    )

# Commit the changes and close the connection
conn.commit()
conn.close()

if documents:
    # Retrieves the first document from the documents list and stores it in first_document
    first_document = documents[0]
    print("Content:", first_document.page_content)
    print("Metadata:", first_document.metadata)
else:
    print("No documents loaded.")

# Configure the instance of the GoogleGenerativeAI class
llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)
