from langchain.prompts import PromptTemplate


def get_prompt_template():
    """
    Returns a LangChain PromptTemplate for question answering with context.
    """
    template = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. "
        "Use three sentences maximum and keep the answer concise.\n\n"
        "{history}\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    )
    return PromptTemplate(
        input_variables=["context", "question", "history"],
        template=template,
    )
