import streamlit as st
import chromadb
def init_session_state():
    defaults = {
        "pdf_processed": False,
        "pdf_text": None,
        "chunks": None,
        "embeddings": None,
        "chat_history": [],
        "notes": [],
        "flashcards": [],
        "quiz_questions": [],
        "interview_questions": [],
        "pdf_name": "",
        "pdf_pages": 0,
        "total_chars": 0,
        "chunk_count": 0,
        "chunk_size": 500,
        "chunk_overlap": 100,
        "model_name": "llama-3.3-70b-versatile",
        "embedding_model": "all-MiniLM-L6-v2",
        "db_path": "./chroma_db",
        "collection_name": "pdf_chatbot",
        "n_results": 3,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
@st.cache_resource
def get_collection():
    """Connect to ChromaDB safely without storing in session state."""
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        return client.get_collection("pdf_chatbot")
    except Exception:
        return client.get_or_create_collection("pdf_chatbot")
