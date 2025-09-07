# Import necessary libraries
import os


# Define a function to get the API key
def get_api_key():
    # Get the API key from the .env file
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set GOOGLE_API_KEY in the .env file."
        )
    return api_key
