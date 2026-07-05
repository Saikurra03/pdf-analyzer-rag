import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
st.set_page_config(page_title="RAG Configuration", page_icon="🔧", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">🔧 RAG Configuration</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Fine-tune your Retrieval-Augmented Generation pipeline</div>', unsafe_allow_html=True)
st.subheader("🧩 Chunking Parameters")
col1, col2 = st.columns(2)
with col1:
    new_chunk_size = st.slider("Chunk Size (characters)", 100, 2000, st.session_state.chunk_size, step=50)
with col2:
    new_overlap = st.slider("Chunk Overlap (characters)", 0, 500, st.session_state.chunk_overlap, step=25)
st.caption("⚠️ Changing these requires re-processing the PDF from the Settings page.")
st.divider()
st.subheader("🔍 Retrieval Parameters")
new_n_results = st.slider("Top-K Results", 1, 10, st.session_state.n_results)
st.session_state.n_results = new_n_results
st.success(f"Top-K updated to {new_n_results} (applied immediately for search)")
st.divider()
st.subheader("🗄️ Vector Database")
col1, col2 = st.columns(2)
with col1:
    st.text_input("DB Path", value=st.session_state.db_path, disabled=True)
with col2:
    st.text_input("Collection Name", value=st.session_state.collection_name, disabled=True)
st.caption("To change the database path or collection, modify `config.py` and restart the app.")
st.divider()
st.subheader("📝 Prompt Template Preview")
from utils.prompt_builder import build_prompt
sample_prompt = build_prompt("What is the main topic?", ["Sample chunk 1", "Sample chunk 2"])
with st.expander("View current prompt template"):
    st.code(sample_prompt, language="markdown")
st.divider()
st.subheader("💾 Save Configuration")
if st.button("Apply & Save", type="primary", use_container_width=True):
    st.session_state.chunk_size = new_chunk_size
    st.session_state.chunk_overlap = new_overlap
    st.success("✅ Configuration saved! Re-process PDF to apply chunking changes.")
