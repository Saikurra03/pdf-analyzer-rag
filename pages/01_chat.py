import streamlit as st
from components.session import init_session_state, get_collection
from components.styles import inject_custom_css
from components.navigation import show_navigation
st.set_page_config(page_title="AI Chat", page_icon="💬", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">💬 AI Chat Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Ask questions about your uploaded PDF</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from utils.retriever import semantic_search
from utils.prompt_builder import build_prompt
from utils.gemini_llm import generate_answer
collection = get_collection()
# Chat history display
for msg in st.session_state.chat_history:
    role, text = msg
    if role == "user":
        st.markdown(f'<div class="chat-user">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai">{text}</div>', unsafe_allow_html=True)
# Input
question = st.chat_input("Ask a question about your PDF...")
if question:
    st.session_state.chat_history.append(("user", question))
    st.markdown(f'<div class="chat-user">{question}</div>', unsafe_allow_html=True)
    with st.spinner("🔍 Searching & generating answer..."):
        try:
            retrieved = semantic_search(collection, question)
            prompt = build_prompt(question, retrieved)
            answer = generate_answer(prompt)
            st.session_state.chat_history.append(("ai", answer))
            st.markdown(f'<div class="chat-ai">{answer}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")
if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
