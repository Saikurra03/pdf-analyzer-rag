import streamlit as st
from components.session import init_session_state, get_collection
from components.styles import inject_custom_css
from components.navigation import show_navigation

st.set_page_config(page_title="PDF Chatbot", page_icon="📚", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()

# ===========================================
# Hero Section
# ===========================================

st.markdown("""
<div class="hero-section">
    <div class="hero-title">📚 PDF Chatbot</div>
    <div class="hero-subtitle">Upload a PDF, ask questions, get instant AI-powered answers</div>
</div>
""", unsafe_allow_html=True)

# ===========================================
# Feature Cards
# ===========================================

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">AI Chat</div>
        <div class="feature-desc">Ask questions about your PDF</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Summarize</div>
        <div class="feature-desc">Get instant summaries</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🃏</div>
        <div class="feature-title">Flashcards</div>
        <div class="feature-desc">Generate study cards</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">❓</div>
        <div class="feature-title">Quiz</div>
        <div class="feature-desc">Test your knowledge</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===========================================
# PDF Upload & Processing
# ===========================================

if st.session_state.pdf_processed:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #43A04722, #43A04711);
        border: 1px solid #43A04744;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <span style="font-size: 24px;">✅</span>
        <div>
            <div style="font-weight: 700; color: #43A047;">PDF Ready: {st.session_state.pdf_name}</div>
            <div style="font-size: 13px; color: #888;">{st.session_state.pdf_pages} pages · {st.session_state.chunk_count} chunks created</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Start Chatting", use_container_width=True):
            st.switch_page("pages/01_chat.py")
    with col2:
        if st.button("📝 Generate Summary", use_container_width=True):
            st.switch_page("pages/02_summary.py")
    with col3:
        if st.button("⚙️ Change Settings", use_container_width=True):
            st.switch_page("pages/11_settings.py")

else:
    st.subheader("📄 Upload Your PDF")
    st.markdown("Upload a PDF file to get started. The document will be processed and indexed for AI-powered Q&A.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Max file size: 200MB"
    )

    if uploaded_file is not None:
        st.markdown(f"""
        <div style="
            background: #1E88E511;
            border: 1px solid #1E88E533;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
        ">
            <strong>📎 {uploaded_file.name}</strong> ({uploaded_file.size / 1024:.1f} KB)
        </div>
        """, unsafe_allow_html=True)

        chunk_size = st.slider("Chunk Size", 100, 2000, 500, step=50)
        chunk_overlap = st.slider("Chunk Overlap", 0, 500, 100, step=25)

        if st.button("🚀 Process PDF", use_container_width=True, type="primary"):
            with st.spinner("Reading PDF..."):
                from utils.pdf_reader import read_pdf
                import tempfile
                import os

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                text = read_pdf(tmp_path)
                os.unlink(tmp_path)

            st.success(f"PDF read successfully! ({len(text)} characters)")

            with st.spinner("Splitting into chunks..."):
                from utils.chunking import create_chunks
                chunks = create_chunks(text, chunk_size=chunk_size, overlap=chunk_overlap)

            st.success(f"Created {len(chunks)} chunks")

            with st.spinner("Generating embeddings..."):
                from utils.embeddings import generate_embeddings
                embeddings = generate_embeddings(chunks)

            with st.spinner("Storing in vector database..."):
                from utils.vector_db import store_in_chromadb
                collection = store_in_chromadb(chunks, embeddings)

            # Store in session state
            st.session_state.pdf_processed = True
            st.session_state.pdf_text = text
            st.session_state.chunks = chunks
            st.session_state.embeddings = embeddings
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.pdf_pages = len(chunks)
            st.session_state.total_chars = len(text)
            st.session_state.chunk_count = len(chunks)
            st.session_state.chunk_size = chunk_size
            st.session_state.chunk_overlap = chunk_overlap

            st.balloons()
            st.rerun()

# ===========================================
# Quick Stats (when PDF is loaded)
# ===========================================

if st.session_state.pdf_processed:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Quick Stats")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Characters", f"{st.session_state.total_chars:,}")
    c2.metric("Chunks", st.session_state.chunk_count)
    c3.metric("Model", "Llama 3.3 70B")
    c4.metric("Embeddings", "MiniLM-L6-v2")
