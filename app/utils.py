"""
Utility functions for text processing
"""

def chunk_text(text, size=1024, overlap=0):
    """Split text into chunks"""
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunk = text[i:i + size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def clean_text(text):
    """Clean and normalize text"""
    text = text.strip()
    text = " ".join(text.split())
    return text
