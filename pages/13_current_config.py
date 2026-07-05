import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
from components.cards import metric_card
st.set_page_config(page_title="Current Configuration", page_icon="📋", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">📋 Current Configuration</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Complete view of all active settings and session state</div>', unsafe_allow_html=True)
st.subheader("📄 Document Status")
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("PDF Loaded", "✅ Yes" if st.session_state.pdf_processed else "❌ No", "📄", "#43A047" if st.session_state.pdf_processed else "#E53935")
with col2:
    metric_card("PDF Name", st.session_state.pdf_name or "N/A", "📝", "#1E88E5")
with col3:
    metric_card("Pages", st.session_state.pdf_pages or "N/A", "📃", "#FB8C00")
with col4:
    metric_card("Characters", f"{st.session_state.total_chars:,}" if st.session_state.total_chars else "N/A", "🔤", "#8E24AA")
st.divider()
st.subheader("🧠 Model Configuration")
model_data = [
    ("LLM Model", st.session_state.model_name),
    ("Embedding Model", st.session_state.embedding_model),
]
for label, value in model_data:
    col_icon, col_text = st.columns([0.05, 0.95])
    with col_icon:
        st.markdown("🟢")
    with col_text:
        st.markdown(f"**{label}**: `{value}`")
st.divider()
st.subheader("🧩 Chunking Configuration")
chunk_data = [
    ("Chunk Size", f"{st.session_state.chunk_size} characters"),
    ("Chunk Overlap", f"{st.session_state.chunk_overlap} characters"),
    ("Total Chunks", st.session_state.chunk_count if st.session_state.chunk_count else "N/A"),
]
for label, value in chunk_data:
    col_icon, col_text = st.columns([0.05, 0.95])
    with col_icon:
        st.markdown("🟢")
    with col_text:
        st.markdown(f"**{label}**: `{value}`")
st.divider()
st.subheader("🔍 Retrieval Configuration")
retrieval_data = [
    ("Top-K Results", st.session_state.n_results),
    ("Similarity Metric", "Cosine (via ChromaDB default)"),
]
for label, value in retrieval_data:
    col_icon, col_text = st.columns([0.05, 0.95])
    with col_icon:
        st.markdown("🟢")
    with col_text:
        st.markdown(f"**{label}**: `{value}`")
st.divider()
st.subheader("🗄️ Vector Database")
db_data = [
    ("Database Path", st.session_state.db_path),
    ("Collection Name", st.session_state.collection_name),
    ("Database Type", "ChromaDB (Persistent)"),
]
for label, value in db_data:
    col_icon, col_text = st.columns([0.05, 0.95])
    with col_icon:
        st.markdown("🟢")
    with col_text:
        st.markdown(f"**{label}**: `{value}`")
st.divider()
st.subheader("💬 Session Data")
session_data = [
    ("Chat Messages", len(st.session_state.chat_history)),
    ("Saved Notes", len(st.session_state.notes)),
    ("Flash Cards", len(st.session_state.flashcards)),
    ("Quiz Questions", len(st.session_state.quiz_questions)),
    ("Interview Questions", len(st.session_state.interview_questions)),
]
for label, value in session_data:
    col_icon, col_text = st.columns([0.05, 0.95])
    with col_icon:
        st.markdown("🟢")
    with col_text:
        st.markdown(f"**{label}**: `{value}`")
