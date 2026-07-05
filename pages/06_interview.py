import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
st.set_page_config(page_title="Interview Questions", page_icon="🎯", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">🎯 Interview Questions</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">AI-generated interview prep from your PDF</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from utils.gemini_llm import generate_answer
import json
difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced", "Mixed"])
num_q = st.slider("Number of questions", 3, 15, 5)
focus = st.text_input("Focus area (optional)", placeholder="e.g., algorithms, system design")
if st.button("🎯 Generate Interview Questions", type="primary", use_container_width=True):
    text = st.session_state.pdf_text[:6000]
    prompt = f"""Generate {num_q} {difficulty}-level interview questions based on this document{f' focusing on {focus}' if focus else ''}.
Return ONLY valid JSON array (no markdown, no code blocks):
[{{"question": "...", "expected_answer": "...", "follow_up": "..."}}]
Document:
{text}"""
    with st.spinner("🧠 Generating interview questions..."):
        try:
            raw = generate_answer(prompt)
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
                cleaned = cleaned.rsplit("```", 1)[0]
            questions = json.loads(cleaned)
            st.session_state.interview_questions = questions
            st.success(f"✅ Generated {len(questions)} questions!")
        except Exception as e:
            st.error(f"Failed to parse: {e}\n\nRaw:\n{raw}")
if st.session_state.interview_questions:
    st.divider()
    for i, q in enumerate(st.session_state.interview_questions):
        with st.expander(f"Q{i+1}: {q['question'][:80]}..."):
            st.markdown(f"**Question:** {q['question']}")
            st.markdown(f"**Expected Answer:** {q.get('expected_answer', 'N/A')}")
            st.markdown(f"**Follow-up:** {q.get('follow_up', 'N/A')}")
    if st.button("🗑️ Clear Questions"):
        st.session_state.interview_questions = []
        st.rerun()
elif not st.session_state.interview_questions and st.session_state.pdf_processed:
    st.info("👆 Generate interview questions using the controls above.")
