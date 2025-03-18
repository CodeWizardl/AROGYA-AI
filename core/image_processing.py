import base64
import os
from core.api_client import get_groq_client

def encode_image(image_path):
    """Converts an image to a base64-encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        raise ValueError("Image file not found.")
    except Exception as e:
        raise RuntimeError(f"Error encoding image: {e}")

def analyze_image_with_query(query, model, image_path):
    """Analyzes an image using Groq's multimodal LLM."""
    encoded_image = encode_image(image_path)
    client = get_groq_client()
    
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": query},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
        ]}
    ]
    
    response = client.chat.completions.create(messages=messages, model=model)
    return response.choices[0].message.content if response.choices else "No response from model."
