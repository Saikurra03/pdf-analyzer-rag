import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
from components.charts import chunk_distribution_chart
st.set_page_config(page_title="Embedding Info", page_icon="🧬", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">🧬 Embedding Information</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Details about the embedding model and generated embeddings</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from components.cards import metric_card
col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Model", st.session_state.embedding_model, "🧠", "#1E88E5")
with col2:
    metric_card("Total Embeddings", st.session_state.chunk_count, "🔢", "#43A047")
with col3:
    if st.session_state.embeddings is not None:
        dim = len(st.session_state.embeddings[0])
        metric_card("Embedding Dimension", dim, "📏", "#8E24AA")
    else:
        metric_card("Embedding Dimension", "N/A", "📏", "#8E24AA")
st.divider()
if st.session_state.embeddings is not None:
    st.subheader("📊 Chunk Size Distribution")
    chunk_distribution_chart(st.session_state.chunks)
    st.subheader("🔬 Sample Embedding Values")
    idx = st.slider("Select chunk", 0, st.session_state.chunk_count - 1, 0)
    emb = st.session_state.embeddings[idx]
    st.markdown(f"**Chunk {idx+1}** — First 20 values:")
    st.code(str([round(float(v), 6) for v in emb[:20]]), language="python")
    st.markdown(f"Total dimensions: `{len(emb)}`")
else:
    st.info("Embeddings not stored in session. Re-process the PDF from Settings to capture embeddings.")
