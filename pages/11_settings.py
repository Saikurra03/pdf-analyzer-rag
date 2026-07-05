import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()

st.markdown('<div class="page-title">⚙️ Settings</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Configure model parameters and reset the application</div>', unsafe_allow_html=True)

st.subheader("🧠 Model Configuration")
col1, col2 = st.columns(2)
with col1:
    st.session_state.model_name = st.selectbox(
        "LLM Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )
with col2:
    st.session_state.embedding_model = st.selectbox(
        "Embedding Model",
        ["all-MiniLM-L6-v2", "all-mpnet-base-v2"],
        index=0
    )

st.divider()

if st.session_state.pdf_processed:
    st.success(f"Currently loaded: **{st.session_state.pdf_name}**")
    if st.button("🔄 Reset — Remove PDF and start over"):
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
        for key in list(st.session_state.keys()):
            if key in defaults:
                del st.session_state[key]
        init_session_state()
        st.rerun()
else:
    st.info("No PDF loaded. Go to the **Home** page to upload one.")
