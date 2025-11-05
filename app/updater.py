"""
Script to periodically update the knowledge base with new data
"""
from vector_db import add_doc
from data_sources import fetch_new_data
import time

def update_knowledge_base():
    """Fetch and add new documents to the knowledge base"""
    new_texts = fetch_new_data()
    for text in new_texts:
        try:
            add_doc(text)
        except Exception as e:
            print(f"Error adding document: {e}")
    
    print(f"✅ {len(new_texts)} new documents ingested.")

if __name__ == "__main__":
    update_knowledge_base()
