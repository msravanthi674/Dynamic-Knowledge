import streamlit as st
from dotenv import load_dotenv
import os
import time

load_dotenv()

from chatbot import get_chatbot_response
from vector_db import add_doc, add_docs_batch, get_kb_stats, clear_knowledge_base
from data_sources import save_uploaded_file, extract_zip_dataset, load_uploaded_datasets

API_KEY = os.getenv("MISTRAL_API_KEY")
print(f"[DEBUG] MISTRAL_API_KEY in main.py: '{API_KEY[:10]}...'")

st.set_page_config(page_title="Dynamic KB Chatbot", layout="wide")
st.title("Dynamic Knowledge Base Chatbot")
st.markdown("---")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "kb_initialized" not in st.session_state:
    st.session_state.kb_initialized = True

# Sidebar with dataset upload and management
with st.sidebar:
    st.title("📚 Knowledge Base Management")
    
    # Show KB stats
    stats = get_kb_stats()
    st.metric("Documents in KB", stats["num_documents"])
    st.metric("Index Size", f"{stats['total_size_kb']:.2f} KB")
    
    st.markdown("---")
    
    # Dataset upload section
    st.subheader("📤 Upload Custom Dataset")
    uploaded_file = st.file_uploader(
        "Upload ZIP file with dataset",
        type=['zip'],
        help="ZIP file can contain JSON, CSV, or TXT files"
    )
    
    if uploaded_file is not None:
        if st.button("📥 Load Dataset", key="load_dataset"):
            with st.spinner("Processing ZIP file..."):
                try:
                    # Save uploaded file
                    file_path = save_uploaded_file(uploaded_file)
                    
                    # Extract and parse ZIP
                    texts = extract_zip_dataset(file_path)
                    
                    if texts:
                        st.info(f"Found {len(texts)} documents in ZIP file")
                        
                        # Add to knowledge base
                        with st.spinner(f"Adding {len(texts)} documents to knowledge base..."):
                            added = add_docs_batch(texts)
                            st.success(f"✅ Successfully added {added} documents!")
                    else:
                        st.warning("No documents found in ZIP file")
                
                except Exception as e:
                    st.error(f"❌ Error processing ZIP: {e}")
    
    st.markdown("---")
    
    # Load existing datasets
    if st.button("📂 Load Existing Datasets"):
        with st.spinner("Loading uploaded datasets..."):
            try:
                texts = load_uploaded_datasets()
                if texts:
                    added = add_docs_batch(texts)
                    st.success(f"✅ Loaded {added} documents from existing datasets!")
                else:
                    st.info("No datasets found in upload directory")
            except Exception as e:
                st.error(f"❌ Error loading datasets: {e}")
    
    st.markdown("---")
    
    # Knowledge base management
    st.subheader("⚙️ KB Management")
    if st.button("🗑️ Clear Knowledge Base", key="clear_kb"):
        clear_knowledge_base()
        st.success("✅ Knowledge base cleared!")
        st.rerun()

# Main chat area
st.subheader("💬 Chat History")
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        with st.container():
            st.markdown(f"**👤 You:** {chat['user']}")
            st.markdown(f"**🤖 Bot:** {chat['bot']}")
            st.markdown("---")
else:
    st.info("No messages yet. Start by uploading a dataset or asking a sample question!")

# User input section
st.subheader("❓ Ask a Question")
user_input = st.text_input("Enter your question:", placeholder="E.g., What is the tallest mountain?")

# Handle input from either text box or sidebar button
question_to_process = user_input if user_input else None

if question_to_process:
    # Prevent repeated answers for same consecutive question
    last_user_message = st.session_state.chat_history[-1]['user'] if st.session_state.chat_history else None
    
    if question_to_process != last_user_message:
        with st.spinner("Generating response..."):
            try:
                response = get_chatbot_response(question_to_process)
                st.session_state.chat_history.append({"user": question_to_process, "bot": response})
                st.rerun()
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    st.error("⏱️ Rate limit exceeded. Please wait a few moments before trying again.")
                else:
                    st.error(f"❌ Error generating response: {e}")
    else:
        st.warning("You already asked this question. Please ask something new.")
