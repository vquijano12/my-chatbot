from langchain_google_genai import ChatGoogleGenerativeAI


def get_chat_model():
    return ChatGoogleGenerativeAI(model="gemini-2.5-pro")


def generate_response(prompt):
    llm = get_chat_model()
    return llm.invoke(prompt)
