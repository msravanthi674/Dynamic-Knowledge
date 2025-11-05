import os
import requests
import numpy as np
import faiss
import time
import json
import pickle
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
print(f"[DEBUG] MISTRAL_API_KEY in vector_db.py: '{API_KEY[:10]}...'")

if not API_KEY:
    raise ValueError("MISTRAL_API_KEY environment variable is not set!")

BASE_URL = "https://api.mistral.ai/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

DB_DIM = 1024

# Create persistence directory
DB_DIR = "data/knowledge_base"
Path(DB_DIR).mkdir(parents=True, exist_ok=True)

INDEX_PATH = os.path.join(DB_DIR, "index.faiss")
DOCSTORE_PATH = os.path.join(DB_DIR, "docstore.pkl")

# Load or initialize index
if os.path.exists(INDEX_PATH) and os.path.exists(DOCSTORE_PATH):
    print("[INFO] Loading existing knowledge base...")
    index = faiss.read_index(INDEX_PATH)
    with open(DOCSTORE_PATH, 'rb') as f:
        docstore = pickle.load(f)
else:
    print("[INFO] Creating new knowledge base...")
    index = faiss.IndexFlatL2(DB_DIM)
    docstore = []

def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

session = create_session_with_retries()

def embed_text(text, max_retries=3):
    """Generate embeddings with retry logic"""
    payload = {
        "model": "mistral-embed",
        "input": text
    }
    
    for attempt in range(max_retries):
        try:
            response = session.post(
                f"{BASE_URL}/embeddings",
                json=payload,
                headers=HEADERS,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return np.array(data["data"][0]["embedding"])
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = (2 ** attempt) + 1
                print(f"[WARNING] Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    
    raise Exception("Failed to generate embedding")

def add_doc(text):
    """Add document to knowledge base"""
    if not text or len(text.strip()) < 5:
        return False
    
    emb = embed_text(text)
    index.add(np.array([emb]))
    docstore.append(text)
    
    # Auto-save after each addition
    save_knowledge_base()
    return True

def add_docs_batch(texts):
    """Add multiple documents efficiently"""
    added = 0
    for text in texts:
        if add_doc(text):
            added += 1
            time.sleep(0.1)  # Small delay to avoid rate limiting
    
    print(f"✅ Added {added} documents to knowledge base")
    return added

def save_knowledge_base():
    """Save index and docstore to disk"""
    faiss.write_index(index, INDEX_PATH)
    with open(DOCSTORE_PATH, 'wb') as f:
        pickle.dump(docstore, f)
    print(f"[INFO] Knowledge base saved ({len(docstore)} documents)")

def clear_knowledge_base():
    """Clear entire knowledge base"""
    global index, docstore
    index = faiss.IndexFlatL2(DB_DIM)
    docstore = []
    
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    if os.path.exists(DOCSTORE_PATH):
        os.remove(DOCSTORE_PATH)
    
    print("[INFO] Knowledge base cleared")

def search_relevant_chunks(query, top_k=3):
    """Search for relevant chunks"""
    if len(docstore) == 0:
        return ["No documents in knowledge base yet."]
    
    try:
        query_emb = embed_text(query)
        _, I = index.search(np.array([query_emb]), min(top_k, len(docstore)))
        return [docstore[i] for i in I[0] if i < len(docstore)]
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        return ["Error searching knowledge base."]

def get_kb_stats():
    """Get knowledge base statistics"""
    return {
        "num_documents": len(docstore),
        "index_dimension": DB_DIM,
        "total_size_kb": os.path.getsize(INDEX_PATH) / 1024 if os.path.exists(INDEX_PATH) else 0
    }
