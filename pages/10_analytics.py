import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
from components.charts import chunk_distribution_chart
from components.cards import metric_card
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">📈 Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Insights and statistics about your document and RAG pipeline</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
chunks = st.session_state.chunks
embeddings = st.session_state.embeddings
text = st.session_state.pdf_text
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Words", f"{len(text.split()):,}", "📝", "#1E88E5")
with col2:
    metric_card("Sentences", f"{text.count('.') + text.count('!') + text.count('?'):,}", "📄", "#43A047")
with col3:
    metric_card("Avg Chunk Size", f"{np.mean([len(c) for c in chunks]):.0f} chars", "🧩", "#FB8C00")
with col4:
    metric_card("Chat Messages", f"{len(st.session_state.chat_history)}", "💬", "#8E24AA")
st.divider()
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("📊 Chunk Size Distribution")
    chunk_distribution_chart(chunks)
with col_right:
    st.subheader("📊 Word Frequency (Top 20)")
    words = text.lower().split()
    from collections import Counter
    stop_words = set(["the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "shall", "can", "to", "of", "in", "for", "on", "with", "at", "by", "from", "as", "into", "through", "during", "before", "after", "above", "below", "between", "out", "off", "over", "under", "again", "further", "then", "once", "and", "but", "or", "nor", "not", "so", "if", "it", "its", "this", "that", "these", "those", "i", "me", "my", "we", "our", "you", "your", "he", "him", "his", "she", "her", "they", "them", "their", "what", "which", "who", "whom", "when", "where", "why", "how", "all", "each", "every", "both", "few", "more", "most", "other", "some", "such", "no", "only", "own", "same", "than", "too", "very", "just", "about", "also"])
    filtered = [w for w in words if w.isalpha() and w not in stop_words and len(w) > 2]
    top_words = Counter(filtered).most_common(20)
    if top_words:
        fig = px.bar(x=[w for w, c in top_words], y=[c for w, c in top_words], labels={"x": "Word", "y": "Count"}, color_discrete_sequence=["#8E24AA"])
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
if embeddings is not None:
    st.divider()
    st.subheader("🧬 Embedding Statistics")
    emb_array = np.array(embeddings)
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Mean", f"{np.mean(emb_array):.6f}", "📊", "#1E88E5")
    with col2:
        metric_card("Std Dev", f"{np.std(emb_array):.6f}", "📊", "#43A047")
    with col3:
        metric_card("Min / Max", f"{np.min(emb_array):.4f} / {np.max(emb_array):.4f}", "📊", "#FB8C00")
