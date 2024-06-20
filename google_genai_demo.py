import os
import json
import sqlite3
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set GOOGLE_GENAI_API_KEY in the .env file."
    )


loader = TextLoader("docs/urban_oasis.txt")
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
docs = text_splitter.split_documents(documents)


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


embeddings = [embeddings.embed_query(doc.page_content) for doc in docs]


conn = sqlite3.connect("genai_embeddings.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, document TEXT, embedding TEXT)"""
)


for doc, embedding in zip(documents, embeddings):
    embedding_json = json.dumps(embedding)
    c.execute(
        "INSERT INTO documents (document, embedding) VALUES (?, ?)",
        (doc.page_content, embedding_json),
    )


conn.commit()
conn.close()

if documents:
    first_document = documents[0]
    print("Content:", first_document.page_content)
    print("Metadata:", first_document.metadata)
else:
    print("No documents loaded.")


from langchain_google_genai import HarmBlockThreshold, HarmCategory

llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)
