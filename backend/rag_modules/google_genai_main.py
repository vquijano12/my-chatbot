import os
from dotenv import load_dotenv
from google_genai_document_processing import load_and_process_documents


def main():
    filepaths = []
    # Load environment variables from .env at the root of backend
    backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(backend_root, ".env"))

    # Use backend_root to get the raw_documents directory (located at backend/raw_documents)
    directory = os.path.join(backend_root, "raw_documents")

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # Check if it is a file
        if os.path.isfile(f):
            print("The filename is:", f)
            filepaths.append(f)

    # Debugging: Print the current working directory
    print(f"Current working directory: {os.getcwd()}")

    # Process and insert documents
    load_and_process_documents(filepaths)


if __name__ == "__main__":
    main()
