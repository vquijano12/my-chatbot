import os
from google_genai_document_processing import load_and_process_documents


def main():
    filepaths = []

    directory = "docs"

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
