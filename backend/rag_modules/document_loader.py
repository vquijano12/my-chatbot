from langchain_community.document_loaders import TextLoader


def load_documents(filepaths):
    """
    Loads documents from a list of file paths.
    Returns a list of loaded documents.
    """
    documents = []
    for filepath in filepaths:
        loader = TextLoader(filepath)
        docs = loader.load()
        documents.extend(docs)
    return documents
