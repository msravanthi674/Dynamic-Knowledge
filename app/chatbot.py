import os
import requests
from vector_db import search_relevant_chunks
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
print(f"[DEBUG] MISTRAL_API_KEY in chatbot.py: '{API_KEY[:10]}...'")

if not API_KEY:
    raise ValueError("MISTRAL_API_KEY environment variable is not set!")

BASE_URL = "https://api.mistral.ai/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODEL_NAME = "mistral-small"

def get_chatbot_response(query):
    retrieved_chunks = search_relevant_chunks(query)
    context = "\n".join(retrieved_chunks)
    
    # Check if we have relevant context
    has_context = "No documents in knowledge base" not in context

    system_prompt = (
        f"You are a helpful assistant. Use the following context to answer questions:\n{context}\n\n"
        f"If the context doesn't contain relevant information, you may provide general knowledge, "
        f"but always indicate when you're using general knowledge vs the provided context."
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }

    response = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
