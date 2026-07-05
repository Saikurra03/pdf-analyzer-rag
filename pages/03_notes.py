import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
st.set_page_config(page_title="Notes", page_icon="📒", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">📒 Notes</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Take and manage notes from your PDF analysis</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from utils.gemini_llm import generate_answer
tab_add, tab_view = st.tabs(["➕ Add Note", "📖 All Notes"])
with tab_add:
    note_title = st.text_input("Note Title", placeholder="e.g., Key concepts from Chapter 3")
    note_mode = st.radio("Mode", ["Manual", "AI-Generated from Topic"])
    if note_mode == "Manual":
        note_content = st.text_area("Note Content", height=200, placeholder="Write your note here...")
    else:
        topic = st.text_input("Topic to generate notes about", placeholder="e.g., Explain neural networks")
        if st.button("🤖 Generate Note", type="primary"):
            if topic and st.session_state.pdf_text:
                with st.spinner("Generating notes..."):
                    prompt = f"Create detailed study notes about '{topic}' based on this document:\n\n{st.session_state.pdf_text[:6000]}"
                    note_content = generate_answer(prompt)
                    st.text_area("Generated Note", value=note_content, height=200)
            else:
                st.warning("Enter a topic first.")
                note_content = ""
    if st.button("💾 Save Note", use_container_width=True):
        if note_title and note_content:
            st.session_state.notes.append({"title": note_title, "content": note_content})
            st.success("✅ Note saved!")
            st.rerun()
        else:
            st.warning("Fill in both title and content.")
with tab_view:
    if not st.session_state.notes:
        st.info("📭 No notes yet. Add your first note above.")
    else:
        for i, note in enumerate(st.session_state.notes):
            with st.expander(f"📒 {note['title']}"):
                st.markdown(note["content"])
                if st.button("🗑️ Delete", key=f"del_note_{i}"):
                    st.session_state.notes.pop(i)
                    st.rerun()
