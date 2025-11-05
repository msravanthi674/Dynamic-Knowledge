import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
print(f"API Key loaded: {API_KEY[:10]}...")
print(f"API Key length: {len(API_KEY) if API_KEY else 0}")

if not API_KEY:
    print("ERROR: API Key is not set!")
    exit(1)

BASE_URL = "https://api.mistral.ai/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Test embeddings with correct format
payload = {
    "model": "mistral-embed",
    "input": "Hello world"  # Singular "input" with string value
}

print("\nTesting Mistral Embeddings API...")
print(f"URL: {BASE_URL}/embeddings")
print(f"Payload: {payload}\n")

response = requests.post(f"{BASE_URL}/embeddings", json=payload, headers=HEADERS)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}\n")

if response.status_code == 200:
    print("✅ API Key is valid! Your setup should work.")
else:
    print("❌ API request failed.")
