import os
from groq import Groq

def get_groq_client():
    """Creates and returns a Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is missing from environment variables.")
    return Groq(api_key=api_key)
