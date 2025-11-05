# 🧠 Dynamic Knowledge Base Chatbot

A **powerful retrieval-augmented generation (RAG)** chatbot powered by **Mistral AI** and **FAISS**, designed to dynamically ingest, search, and respond using documents from **custom or general knowledge datasets**.  
Built with **Streamlit** for an interactive and user-friendly interface.

---

## 🚀 Features

- **🔍 Vector Semantic Search:** Semantic text search using FAISS for efficient retrieval.
- **🤖 Mistral AI Integration:** Uses Mistral's embedding and chat models for rich interactions.
- **📚 Dynamic Knowledge Base:** Upload, manage, and dynamically update knowledge bases including custom datasets in ZIP format.
- **⚡ Hybrid Knowledge Mode:** Answers based on ingested data or falls back to general knowledge with clear indication.
- **💬 Streamlit-powered UI:** Clean, modern, responsive interface with chat history and dataset management.
- **⏳ Rate Limiting and Retry Logic:** Handles Mistral API rate limits gracefully.
- **💾 Persistent Storage:** Vector index and knowledge base documents persist across sessions.

---

## 🏗️ Project Structure
```bash
app/
├── main.py # Streamlit UI and orchestration
├── chatbot.py # Chat response generation (Mistral chat API)
├── vector_db.py # Vector database operations using FAISS
├── data_sources.py # Dataset ingestion and ZIP dataset parsing
├── updater.py # Periodic knowledge base update script
├── utils.py # Utility functions for text processing
├── kaggle_downloader.py # Script to download datasets from Kaggle
├── data_loader.py # Loader to process downloaded Kaggle datasets
└── init.py # Package initialization
data/
├── uploads/ # User uploaded ZIP datasets
└── knowledge_base/ # Persisted FAISS index and documents
.env # Environment variables (API keys, etc)
requirements.txt # Package dependencies
README.md # Project documentation (this file)
```
---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/chatbot-dynamic-kb.git
cd chatbot-dynamic-kb
```
### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Create .env File
```bash
MISTRAL_API_KEY=your_mistral_api_key_here
```
---
## ▶️ Usage
### Run Streamlit App
```bash
streamlit run app/main.py
```
## Upload Datasets
- Upload ZIP files containing JSON, CSV, or TXT knowledge datasets.
- Load existing datasets from the data/uploads folder.
- Clear or update the knowledge base when needed.
- Ask Questions
- Use natural language queries with dynamic context retrieval.
- Answers reflect ingested documents or general knowledge fallback.
---
## Download Kaggle Datasets
```bash
python app/kaggle_downloader.py
```
Use the Kaggle API integration to fetch popular datasets.

---
## ⚠️ Limitations
- API rate limits may apply; rate limiting logic helps mitigate.
- Knowledge base size limited by memory and embedding latency.
- Fallback to general knowledge may not be exhaustive.
---
## 🔮 Future Enhancements
- Persistent vector index storage with incremental updates.
- More robust document chunking and context handling.
- User authentication and multi-user support.
- Advanced query analytics and logging.
- Streaming chat responses for improved UX.
- Integration with more data sources.
--- 
