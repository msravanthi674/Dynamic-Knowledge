import os
import json
import zipfile
import requests
from pathlib import Path

# Directory to store uploaded datasets
UPLOAD_DIR = "data/uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

DATA_SOURCES = [
    "https://storage.googleapis.com/kaggle-data-sets/bitext-gen-ai-chatbot-customer-support-dataset/data.json",
]

def extract_zip_dataset(zip_path):
    """Extract and parse ZIP file containing dataset"""
    results = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all files in zip
            for file_name in zip_ref.namelist():
                # Skip directories and hidden files
                if file_name.endswith('/') or file_name.startswith('.'):
                    continue
                
                # Extract file content
                with zip_ref.open(file_name) as file:
                    content = file.read().decode('utf-8', errors='ignore')
                    
                    # Handle JSON files
                    if file_name.endswith('.json'):
                        try:
                            data = json.loads(content)
                            if isinstance(data, list):
                                for entry in data:
                                    text = extract_text_from_entry(entry)
                                    if text:
                                        results.append(text)
                            elif isinstance(data, dict):
                                text = extract_text_from_entry(data)
                                if text:
                                    results.append(text)
                        except json.JSONDecodeError:
                            pass
                    
                    # Handle CSV files
                    elif file_name.endswith('.csv'):
                        import csv
                        import io
                        reader = csv.DictReader(io.StringIO(content))
                        for row in reader:
                            # Combine all column values into text
                            text = " ".join(str(v) for v in row.values() if v)
                            if text:
                                results.append(text)
                    
                    # Handle TXT files
                    elif file_name.endswith('.txt'):
                        # Split by lines or paragraphs
                        paragraphs = content.split('\n\n')
                        for para in paragraphs:
                            para = para.strip()
                            if para and len(para) > 10:
                                results.append(para)
    
    except Exception as e:
        print(f"Error extracting ZIP: {e}")
    
    return results

def extract_text_from_entry(entry):
    """Extract text from various data formats"""
    if isinstance(entry, str):
        return entry
    elif isinstance(entry, dict):
        # Try common field names
        for key in ['text', 'content', 'question', 'answer', 'description', 'title', 'body']:
            if key in entry and entry[key]:
                return str(entry[key])
        # Fallback: combine all values
        values = [str(v) for v in entry.values() if v]
        return " ".join(values) if values else None
    return None

def fetch_new_data():
    """Fetch new documents from data sources"""
    results = []
    for url in DATA_SOURCES:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list):
                for entry in data:
                    text = extract_text_from_entry(entry)
                    if text:
                        results.append(text)
            elif isinstance(data, dict):
                text = extract_text_from_entry(data)
                if text:
                    results.append(text)
        except Exception as e:
            print(f"Failed to fetch from {url}: {e}")
    
    return results

def load_uploaded_datasets():
    """Load all datasets from upload directory"""
    results = []
    
    if not os.path.exists(UPLOAD_DIR):
        return results
    
    for filename in os.listdir(UPLOAD_DIR):
        if filename.endswith('.zip'):
            zip_path = os.path.join(UPLOAD_DIR, filename)
            texts = extract_zip_dataset(zip_path)
            results.extend(texts)
            print(f"✅ Loaded {len(texts)} documents from {filename}")
    
    return results

def save_uploaded_file(uploaded_file):
    """Save uploaded file to disk"""
    if uploaded_file is None:
        return None
    
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path
