import streamlit as st
from components.session import init_session_state, get_collection
from components.styles import inject_custom_css
from components.navigation import show_navigation
from components.charts import similarity_gauge, distance_bar_chart
st.set_page_config(page_title="Semantic Search", page_icon="🔍", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">🔍 Semantic Search</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Search through your PDF using semantic similarity</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from utils.retriever import semantic_search
import chromadb
collection = get_collection()
query = st.text_input("Search query", placeholder="Type your search query here...")
if query:
    with st.spinner("🔍 Searching..."):
        try:
            # Manual retrieval to get distances
            from config import embedding_model
            query_emb = embedding_model.encode(query).tolist()
            results = collection.query(
                query_embeddings=[query_emb],
                n_results=st.session_state.n_results,
                include=["documents", "distances"]
            )
            documents = results["documents"][0]
            distances = results["distances"][0]
            similarities = [1 - d for d in distances]
            col_chart, col_list = st.columns([1, 2])
            with col_chart:
                if similarities:
                    similarity_gauge(similarities[0])
                distance_bar_chart(distances)
            with col_list:
                for i, (doc, sim) in enumerate(zip(documents, similarities)):
                    st.markdown(f"**Result {i+1}** — Similarity: `{sim:.4f}`")
                    with st.expander("View chunk"):
                        st.text(doc)
                    st.divider()
        except Exception as e:
            st.error(f"Search error: {str(e)}")
