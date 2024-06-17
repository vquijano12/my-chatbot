# Import required modules
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from getpass import getpass
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set GOOGLE_GENAI_API_KEY in the .env file."
    )

loader = TextLoader("docs/urban_oasis.txt")
documents = loader.load()

api_key = os.getenv("GOOGLE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector = embeddings.embed_query("hello, world!")
vector[:5]

if documents:
    first_document = documents[0]
    print("Content:", first_document.page_content)
    print("Metadata:", first_document.metadata)
else:
    print("No documents loaded.")

# llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
# print(llm.invoke("How would I say 'Hello, how are you?' in Spanish?"))

# llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
# print(
#     llm.invoke(
#         "What are some of the pros and cons of Python as a programming language?"
#     )
# )

# # Using in a chain
# from langchain_core.prompts import PromptTemplate

# template = """Question: {question}

# Answer: Let's think step by step."""
# prompt = PromptTemplate.from_template(template)

# chain = prompt | llm

# question = "How much is 2+2?"
# print(chain.invoke({"question": question}))

# # Streaming calls
# import sys

# for chunk in llm.stream("Tell me a short poem about snow"):
#     sys.stdout.write(chunk)
#     sys.stdout.flush()

# Safety Settings
from langchain_google_genai import HarmBlockThreshold, HarmCategory

llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)
