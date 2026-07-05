import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
st.set_page_config(page_title="Flash Cards", page_icon="🃏", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">🃏 Flash Cards</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Create and study flashcards from your PDF</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from utils.gemini_llm import generate_answer
import json
tab_gen, tab_study = st.tabs(["🤖 Generate", "📖 Study"])
with tab_gen:
    num_cards = st.slider("Number of flashcards", 3, 20, 5)
    topic = st.text_input("Topic (optional)", placeholder="Leave empty for general coverage")
    if st.button("🃏 Generate Flashcards", type="primary", use_container_width=True):
        text = st.session_state.pdf_text[:6000]
        prompt = f"""Create {num_cards} flashcards from this document{f' about {topic}' if topic else ''}.
Return ONLY valid JSON in this exact format (no markdown, no code blocks):
[{{"front": "question or term", "back": "answer or definition"}}]
Document:
{text}"""
        with st.spinner("🧠 Generating flashcards..."):
            try:
                raw = generate_answer(prompt)
                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
                    cleaned = cleaned.rsplit("```", 1)[0]
                cards = json.loads(cleaned)
                st.session_state.flashcards = cards
                st.success(f"✅ Generated {len(cards)} flashcards!")
            except Exception as e:
                st.error(f"Failed to parse flashcards: {e}\n\nRaw response:\n{raw}")
with tab_study:
    if not st.session_state.flashcards:
        st.info("📭 No flashcards yet. Generate some first.")
    else:
        st.markdown(f"**{len(st.session_state.flashcards)} cards**")
        for i, card in enumerate(st.session_state.flashcards):
            with st.expander(f"Card {i+1}: {card.get('front', '')[:60]}..."):
                st.markdown(f"**Front:** {card.get('front', 'N/A')}")
                st.markdown(f"**Back:** {card.get('back', 'N/A')}")
        if st.button("🗑️ Clear All Cards"):
            st.session_state.flashcards = []
            st.rerun()
