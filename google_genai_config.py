# Import necessary libraries
import os
from dotenv import load_dotenv

# Load all the variables found as environment variables in the .env file
load_dotenv()


# Define a function to get the API key
def get_api_key():
    # Get the API key from the .env file
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set GOOGLE_GENAI_API_KEY in the .env file."
        )
