import streamlit as st
from components.session import init_session_state, get_collection
from components.styles import inject_custom_css
from components.navigation import show_navigation
from components.cards import metric_card
st.set_page_config(page_title="Vector Database", page_icon="🗄️", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">🗄️ Vector Database</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Inspect and explore your ChromaDB collection</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
import chromadb
import os
collection = get_collection()
if collection:
    data = collection.get(include=["documents", "embeddings"])
    total = len(data["ids"])
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Total Records", total, "📦", "#1E88E5")
    with col2:
        metric_card("Collection", st.session_state.collection_name, "🏷️", "#43A047")
    with col3:
        db_size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, filenames in os.walk(st.session_state.db_path) for f in filenames)
        metric_card("DB Size", f"{db_size / 1024:.1f} KB", "💾", "#FB8C00")
    st.divider()
    st.subheader("📋 Stored Records")
    search_id = st.text_input("Filter by ID (e.g., 0, 1, 2...)", placeholder="Enter chunk ID")
    if search_id.strip():
        try:
            result = collection.get(ids=[search_id.strip()], include=["documents", "embeddings"])
            if result["ids"]:
                st.markdown(f"**ID:** `{result['ids'][0]}`")
                st.markdown(f"**Embedding Dimension:** `{len(result['embeddings'][0])}`")
                st.markdown("**Document Content:**")
                st.text_area("Content", value=result["documents"][0], height=200, label_visibility="collapsed")
            else:
                st.warning("ID not found.")
        except Exception as e:
            st.error(str(e))
    else:
        items_per_page = 5
        page = st.number_input("Page", min_value=1, max_value=max(1, (total + items_per_page - 1) // items_per_page), value=1)
        start = (page - 1) * items_per_page
        end = min(start + items_per_page, total)
        for i in range(start, end):
            with st.expander(f"📄 Chunk ID: {data['ids'][i]} — {len(data['documents'][i])} chars"):
                st.text(data["documents"][i])
                if data["embeddings"][i] is not None:
                    st.caption(f"Embedding dim: {len(data['embeddings'][i])} | First 5: {[round(v, 4) for v in data['embeddings'][i][:5]]}")
        st.caption(f"Showing {start+1}-{end} of {total} records")
else:
    st.error("Could not connect to ChromaDB collection.")
